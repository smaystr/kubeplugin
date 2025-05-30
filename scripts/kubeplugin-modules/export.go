package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

type Metric struct {
	Resource  string `json:"resource"`
	Namespace string `json:"namespace"`
	Name      string `json:"name"`
	CPU       string `json:"cpu"`
	Memory    string `json:"memory"`
}

func main() {
	var (
		resourceType = flag.String("type", "pod", "Resource type (pod/node)")
		namespace    = flag.String("n", "default", "Namespace")
		format       = flag.String("format", "csv", "Output format (csv/json/yaml)")
	)
	flag.Parse()

	metrics, err := getMetrics(*resourceType, *namespace)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error getting metrics: %v\n", err)
		os.Exit(1)
	}

	switch *format {
	case "json":
		exportJSON(metrics)
	case "csv":
		exportCSV(metrics)
	default:
		fmt.Fprintf(os.Stderr, "Unsupported format: %s\n", *format)
		os.Exit(1)
	}
}

func getMetrics(resourceType, namespace string) ([]Metric, error) {
	cmd := exec.Command("kubectl", "top", resourceType)
	if resourceType == "pod" {
		cmd.Args = append(cmd.Args, "-n", namespace)
	}

	output, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	return parseOutput(string(output), resourceType, namespace), nil
}

func parseOutput(output, resourceType, namespace string) []Metric {
	lines := strings.Split(strings.TrimSpace(output), "\n")[1:] // Skip header
	metrics := make([]Metric, 0, len(lines))

	for _, line := range lines {
		fields := strings.Fields(line)
		if len(fields) < 3 {
			continue
		}

		metric := Metric{
			Resource: resourceType,
			Name:     fields[0],
			CPU:      fields[1],
			Memory:   fields[2],
		}

		if resourceType == "pod" {
			metric.Namespace = namespace
		} else {
			metric.Namespace = "-"
		}

		metrics = append(metrics, metric)
	}

	return metrics
}

func exportJSON(metrics []Metric) {
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(metrics); err != nil {
		fmt.Fprintf(os.Stderr, "Error encoding JSON: %v\n", err)
		os.Exit(1)
	}
}

func exportCSV(metrics []Metric) {
	writer := csv.NewWriter(os.Stdout)
	defer writer.Flush()

	// Write header
	header := []string{"Resource", "Namespace", "Name", "CPU", "Memory"}
	if err := writer.Write(header); err != nil {
		fmt.Fprintf(os.Stderr, "Error writing CSV header: %v\n", err)
		os.Exit(1)
	}

	// Write data
	for _, metric := range metrics {
		record := []string{
			metric.Resource,
			metric.Namespace,
			metric.Name,
			metric.CPU,
			metric.Memory,
		}
		if err := writer.Write(record); err != nil {
			fmt.Fprintf(os.Stderr, "Error writing CSV record: %v\n", err)
			os.Exit(1)
		}
	}
}
