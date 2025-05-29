# kubectl kubeplugin

Kubectl plugin для отримання статистики використання ресурсів у Kubernetes.

## Вимоги

- kubectl CLI встановлено та налаштовано
- Доступ до Kubernetes кластера
- metrics-server встановлено в кластері

## Встановлення

### Метод 1: Локальне встановлення

1. Зробіть скрипт виконуваним:
```bash
chmod +x scripts/kubectl-kubeplugin
```

2. Додайте директорію scripts до PATH або скопіюйте файл у директорію з PATH:
```bash
# Варіант 1: Додати до PATH (додайте цей рядок до ~/.bashrc або ~/.zshrc)
export PATH="$PATH:$(pwd)/scripts"

# Варіант 2: Скопіювати в системну директорію
sudo cp scripts/kubectl-kubeplugin /usr/local/bin/
```

### Метод 2: Символічне посилання

```bash
sudo ln -s $(pwd)/scripts/kubectl-kubeplugin /usr/local/bin/kubectl-kubeplugin
```

## Використання

```bash
kubectl kubeplugin <RESOURCE_TYPE> [-n|--namespace <NAMESPACE>]
```

### Параметри

- `RESOURCE_TYPE` - тип ресурсу (pod або node)
- `-n, --namespace` - простір імен Kubernetes (за замовчуванням: default)
- `-h, --help` - показати довідку

### Приклади

1. Отримати статистику для всіх подів у просторі імен kube-system:
```bash
kubectl kubeplugin pod -n kube-system
```

2. Отримати статистику для всіх нод кластера:
```bash
kubectl kubeplugin node
```

3. Отримати статистику для подів у просторі імен default:
```bash
kubectl kubeplugin pod
```

### Формат виводу

Плагін виводить статистику у форматі CSV:
```
Resource, Namespace, Name, CPU, Memory
```

Приклад виводу:
```
pod, kube-system, coredns-5d78c9869d-abcde, 5m, 12Mi
pod, kube-system, etcd-control-plane, 25m, 89Mi
node, -, control-plane, 250m, 1234Mi
```

## Тестування

1. Переконайтесь, що плагін доступний:
```bash
kubectl plugin list | grep kubeplugin
```

2. Перевірте довідку:
```bash
kubectl kubeplugin --help
```

3. Запустіть плагін:
```bash
kubectl kubeplugin pod -n kube-system
```

## Вирішення проблем

### Помилка: "Failed to get metrics"

Переконайтесь, що metrics-server встановлено:
```bash
kubectl get deployment metrics-server -n kube-system
```

Якщо metrics-server не встановлено:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Помилка: "command not found"

Переконайтесь, що:
1. Файл має права на виконання: `chmod +x scripts/kubectl-kubeplugin`
2. Шлях до файлу додано до PATH або файл скопійовано в директорію з PATH 