import numpy as np

def get_weights(matrix):
    """Среднее по строкам нормализованной матрицы"""
    return (matrix / matrix.sum(axis=0)).mean(axis=1)

def check_cr(matrix, weights):
    """Проверка согласованности"""
    n = len(weights)
    aw = matrix @ weights
    lambda_max = np.mean([aw[i]/weights[i] for i in range(n) if weights[i] != 0])
    ci = (lambda_max - n) / (n - 1)
    ri = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45}.get(n, 1.45)
    cr = ci / ri
    return cr, cr <= 0.1

def input_int(prompt, min_val):
    """Ввод целого числа с минимумом"""
    while True:
        try:
            n = int(input(prompt))
            if n >= min_val:
                return n
            print(f"Должно быть ≥{min_val}")
        except ValueError:
            print("Введите целое число")

def input_value(prompt):
    """Безопасный ввод числа"""
    while True:
        try:
            val = input(prompt).strip()
            if '/' in val:
                a, b = val.split('/')
                return float(a) / float(b)
            return float(val)
        except:
            print("Ошибка")

def input_matrix(size, name):
    """Ввод матрицы парных сравнений"""
    print(f"\nМатрица {name} ({size}x{size})")

    matrix = np.eye(size, dtype=float)
    
    for i in range(size):
        for j in range(i + 1, size):
            while True:
                value = input_value(f"  [{i+1},{j+1}]: ")
                if value > 0:
                    matrix[i][j] = value
                    matrix[j][i] = 1.0 / value
                    break
                print("Значение должно быть > 0")
    
    return matrix

def run_ahp():
    print("Выбор университета")

    n = input_int("\nКоличество критериев (≥5): ", 5)
    criteria = [input(f"Критерий {i+1}: ") for i in range(n)]

    m = input_int("\nКоличество альтернатив (≥3): ", 3)
    alternatives = [input(f"Альтернатива {i+1}: ") for i in range(m)]
    
    # Матрица критериев
    crit_mat = input_matrix(n, "критериев")
    crit_w = get_weights(crit_mat)
    
    print("\nВеса критериев:")
    for name, w in zip(criteria, crit_w):
        print(f"  {name}: {w:.3f}")
    
    cr, ok = check_cr(crit_mat, crit_w)
    print(f"CR = {cr:.3f} ({'OK' if ok else 'плохо'})")
    
    # Матрицы альтернатив
    alt_weights = []
    for crit in criteria:
        print(f"\nОценка по '{crit}':")
        mat = input_matrix(m, "альтернатив")
        w = get_weights(mat)
        alt_weights.append(w)
        
        cr, ok = check_cr(mat, w)
        print(f"CR = {cr:.3f} ({'хорошо' if ok else 'плохо'})")

    print("\nРезультаты:")
    global_p = np.zeros(m)
    for i in range(m):
        for j in range(n):
            global_p[i] += alt_weights[j][i] * crit_w[j]
    
    results = sorted(zip(alternatives, global_p), key=lambda x: x[1], reverse=True)
    for rank, (name, score) in enumerate(results, 1):
        print(f"  {rank}. {name}: {score:.3f}")
    
    print(f"\nЛучший выбор: {results[0][0]}")

if __name__ == "__main__":
    run_ahp()