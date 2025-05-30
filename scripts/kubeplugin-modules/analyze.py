#!/usr/bin/env python3
"""
Kubernetes resource usage analyzer
Analyzes patterns and provides recommendations
"""

import sys
import subprocess
import json
import argparse
from typing import Dict, List, Tuple

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Kubernetes resource usage patterns')
    parser.add_argument('resource_type', choices=['pod', 'node'], 
                       help='Type of resource to analyze')
    parser.add_argument('-n', '--namespace', default='default',
                       help='Kubernetes namespace (default: default)')
    parser.add_argument('--threshold-cpu', type=int, default=80,
                       help='CPU usage threshold percentage (default: 80)')
    parser.add_argument('--threshold-memory', type=int, default=85,
                       help='Memory usage threshold percentage (default: 85)')
    parser.add_argument('--format', choices=['json', 'table'], default='table',
                       help='Output format (default: table)')
    return parser.parse_args()

def get_metrics(resource_type: str, namespace: str) -> List[Dict]:
    """Get metrics using kubectl top command"""
    cmd = ['kubectl', 'top', resource_type]
    if resource_type == 'pod':
        cmd.extend(['-n', namespace])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return parse_kubectl_output(result.stdout, resource_type)
    except subprocess.CalledProcessError as e:
        print(f"Error getting metrics: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def parse_kubectl_output(output: str, resource_type: str) -> List[Dict]:
    """Parse kubectl top output into structured data"""
    lines = output.strip().split('\n')[1:]  # Skip header
    metrics = []
    
    for line in lines:
        parts = line.split()
        if resource_type == 'pod':
            metrics.append({
                'name': parts[0],
                'cpu': parse_resource_value(parts[1]),
                'memory': parse_resource_value(parts[2]),
                'type': 'pod'
            })
        else:  # node
            metrics.append({
                'name': parts[0],
                'cpu': parse_resource_value(parts[1]),
                'cpu_percent': parse_percent(parts[2]),
                'memory': parse_resource_value(parts[3]),
                'memory_percent': parse_percent(parts[4]),
                'type': 'node'
            })
    
    return metrics

def parse_resource_value(value: str) -> int:
    """Convert resource value to standard unit (Mi for memory, m for CPU)"""
    if value.endswith('Mi'):
        return int(value[:-2])
    elif value.endswith('Gi'):
        return int(value[:-2]) * 1024
    elif value.endswith('m'):
        return int(value[:-1])
    else:
        return int(value)

def parse_percent(value: str) -> int:
    """Parse percentage value"""
    return int(value.rstrip('%'))

def analyze_metrics(metrics: List[Dict], cpu_threshold: int, memory_threshold: int) -> Dict:
    """Analyze metrics and provide recommendations"""
    analysis = {
        'summary': {},
        'warnings': [],
        'recommendations': []
    }
    
    # Calculate summary statistics
    if metrics:
        total_cpu = sum(m['cpu'] for m in metrics)
        total_memory = sum(m['memory'] for m in metrics)
        
        analysis['summary'] = {
            'total_resources': len(metrics),
            'total_cpu_millicores': total_cpu,
            'total_memory_mi': total_memory,
            'average_cpu_millicores': total_cpu // len(metrics),
            'average_memory_mi': total_memory // len(metrics)
        }
        
        # Check for high usage
        for metric in metrics:
            if 'cpu_percent' in metric and metric['cpu_percent'] > cpu_threshold:
                analysis['warnings'].append(
                    f"{metric['type'].title()} '{metric['name']}' has high CPU usage: {metric['cpu_percent']}%"
                )
            if 'memory_percent' in metric and metric['memory_percent'] > memory_threshold:
                analysis['warnings'].append(
                    f"{metric['type'].title()} '{metric['name']}' has high memory usage: {metric['memory_percent']}%"
                )
        
        # Generate recommendations
        if analysis['warnings']:
            analysis['recommendations'].append(
                "Consider scaling horizontally or vertically to handle the load"
            )
        
        # Check for resource imbalance
        if metrics and len(metrics) > 1:
            cpu_values = [m['cpu'] for m in metrics]
            max_cpu = max(cpu_values)
            min_cpu = min(cpu_values)
            if max_cpu > min_cpu * 3:  # 3x difference
                analysis['recommendations'].append(
                    "Significant CPU usage imbalance detected. Consider load balancing or pod distribution policies"
                )
    
    return analysis

def print_table_format(metrics: List[Dict], analysis: Dict):
    """Print results in table format"""
    print("\n=== RESOURCE METRICS ===")
    print(f"{'Name':<30} {'CPU':<10} {'Memory':<10} {'Status':<10}")
    print("-" * 65)
    
    for metric in metrics:
        status = "OK"
        if 'cpu_percent' in metric and metric['cpu_percent'] > 80:
            status = "HIGH CPU"
        elif 'memory_percent' in metric and metric['memory_percent'] > 85:
            status = "HIGH MEM"
        
        print(f"{metric['name']:<30} {metric['cpu']}m{'':<7} {metric['memory']}Mi{'':<7} {status:<10}")
    
    print("\n=== ANALYSIS SUMMARY ===")
    summary = analysis['summary']
    print(f"Total Resources: {summary.get('total_resources', 0)}")
    print(f"Total CPU: {summary.get('total_cpu_millicores', 0)}m")
    print(f"Total Memory: {summary.get('total_memory_mi', 0)}Mi")
    print(f"Average CPU: {summary.get('average_cpu_millicores', 0)}m")
    print(f"Average Memory: {summary.get('average_memory_mi', 0)}Mi")
    
    if analysis['warnings']:
        print("\n=== WARNINGS ===")
        for warning in analysis['warnings']:
            print(f"⚠️  {warning}")
    
    if analysis['recommendations']:
        print("\n=== RECOMMENDATIONS ===")
        for rec in analysis['recommendations']:
            print(f"💡 {rec}")

def print_json_format(metrics: List[Dict], analysis: Dict):
    """Print results in JSON format"""
    output = {
        'metrics': metrics,
        'analysis': analysis
    }
    print(json.dumps(output, indent=2))

def main():
    args = parse_args()
    
    # Get metrics
    metrics = get_metrics(args.resource_type, args.namespace)
    
    # Analyze metrics
    analysis = analyze_metrics(metrics, args.threshold_cpu, args.threshold_memory)
    
    # Output results
    if args.format == 'json':
        print_json_format(metrics, analysis)
    else:
        print_table_format(metrics, analysis)

if __name__ == '__main__':
    main() 