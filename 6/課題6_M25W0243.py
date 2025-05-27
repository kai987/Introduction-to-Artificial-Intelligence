import math


def normalize_data(data):
    """Min-Max正規化 (講義の例に従って)"""
    # 苦味と酸味のリストを作成
    bitterness = [coffee[1] for coffee in data]
    acidity = [coffee[2] for coffee in data]
    
    # Min-Max値を計算
    bitterness_max = max(bitterness)
    bitterness_min = min(bitterness)
    acidity_max = max(acidity)
    acidity_min = min(acidity)
    
    print("=== データの正規化 ===")
    print(f"苦味: min={bitterness_min}, max={bitterness_max}")
    print(f"酸味: min={acidity_min}, max={acidity_max}")
    print()
    
    # 正規化を実行
    normalized_data = []
    for coffee in data:
        name = coffee[0]
        original_bitterness = coffee[1]
        original_acidity = coffee[2]
        
        # Min-Max正規化: (値 - min) / (max - min)
        normalized_bitterness = (original_bitterness - bitterness_min) / (bitterness_max - bitterness_min)
        normalized_acidity = (original_acidity - acidity_min) / (acidity_max - acidity_min)
        
        normalized_data.append([name, normalized_bitterness, normalized_acidity, original_bitterness, original_acidity])
        
        print(f"{name}: 苦味 {original_bitterness} => {normalized_bitterness:.3f}, 酸味 {original_acidity} => {normalized_acidity:.3f}")
    
    print()
    return normalized_data

def euclidean_distance(point1, point2):
    """ユークリッド距離の計算"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_centroid(cluster):
    """重心の計算"""
    if len(cluster) == 0:
        return [0, 0]
    
    sum_bitterness = sum(point[1] for point in cluster)
    sum_acidity = sum(point[2] for point in cluster)
    
    return [sum_bitterness / len(cluster), sum_acidity / len(cluster)]

def print_clusters(clusters, round_num):
    """クラスターの内容を表示"""
    print(f"=== ラウンド {round_num} - クラスター結果 ===")
    for i, cluster in enumerate(clusters):
        print(f"🔵 クラスター {i+1} ({len(cluster)}個):")
        if len(cluster) > 0:
            for coffee in cluster:
                print(f"  {coffee[0]} (元データ: 苦味{coffee[3]}, 酸味{coffee[4]})")
        else:
            print("  空のクラスター")
        print()

def kmeans_coffee():
    """K平均法メイン関数"""
    print("=" * 50)
    print("🎓 K平均法 - 百万遍コーヒー店の課題")
    print("=" * 50)
    print()
    
    # 元データ（講義の課題3）
    raw_data = [
        ['coffee1', 73, 6],
        ['coffee2', 60, 6],
        ['coffee3', 48, 5],
        ['coffee4', 65, 7],
        ['coffee5', 30, 7],
        ['coffee6', 78, 4],
        ['coffee7', 51, 5]
    ]
    
    print("=== 元データ ===")
    print("コーヒー名   苦味  酸味")
    print("-" * 20)
    for coffee in raw_data:
        print(f"{coffee[0]:<10} {coffee[1]:>3}  {coffee[2]:>3}")
    print()
    
    # データの正規化
    normalized_data = normalize_data(raw_data)
    
    # K平均法の設定
    k = 2  # クラスター数
    max_iterations = 10
    
    # 初期中心点の設定（講義の例に従って）
    center0 = [0.50, 0.25]
    center1 = [0.75, 0.95]
    centroids = [center0, center1]
    
    print("=== K平均法の実行 ===")
    print(f"クラスター数: {k}")
    print(f"初期中心点:")
    print(f"  Center0: [{center0[0]:.2f}, {center0[1]:.2f}]")
    print(f"  Center1: [{center1[0]:.2f}, {center1[1]:.2f}]")
    print()
    
    # K平均法の実行
    for iteration in range(max_iterations):
        print(f"--- ラウンド {iteration + 1} ---")
        
        # クラスターを初期化
        clusters = [[] for _ in range(k)]
        
        # 各データポイントを最も近い中心点に割り当て
        print("距離計算と割り当て:")
        for coffee in normalized_data:
            name = coffee[0]
            point = [coffee[1], coffee[2]]
            
            # 各中心点への距離を計算
            distances = []
            for i, centroid in enumerate(centroids):
                dist = euclidean_distance(point, centroid)
                distances.append(dist)
            
            # 最も近い中心点を見つける
            closest_centroid = distances.index(min(distances))
            clusters[closest_centroid].append(coffee)
            
            print(f"  {name}: dist0={distances[0]:.3f}, dist1={distances[1]:.3f} => クラスター{closest_centroid + 1}")
        
        print()
        
        # クラスター結果を表示
        print_clusters(clusters, iteration + 1)
        
        # 新しい中心点を計算
        new_centroids = []
        print("新しい中心点の計算:")
        for i, cluster in enumerate(clusters):
            centroid = calculate_centroid(cluster)
            new_centroids.append(centroid)
            print(f"  クラスター{i+1}の重心: [{centroid[0]:.3f}, {centroid[1]:.3f}]")
        
        print()
        
        # 収束判定
        converged = True
        for i in range(k):
            if (abs(centroids[i][0] - new_centroids[i][0]) > 0.001 or 
                abs(centroids[i][1] - new_centroids[i][1]) > 0.001):
                converged = False
                break
        
        # 中心点を更新
        centroids = new_centroids
        
        if converged:
            print("🎉 収束しました！")
            break
        else:
            print("📍 中心点を更新して次のラウンドへ")
            print()
    
    # 最終結果の表示
    print("=" * 50)
    print("📊 最終結果")
    print("=" * 50)
    
    cluster_names = ["高苦味グループ", "低苦味グループ"]
    for i, cluster in enumerate(clusters):
        print(f"🔵 クラスター{i+1} ({cluster_names[i]}): {len(cluster)}個")
        for coffee in cluster:
            print(f"  - {coffee[0]} (苦味:{coffee[3]}, 酸味:{coffee[4]})")
        print()
    
    print("✅ K平均法によるクラスタリング完了")

# プログラムの実行
if __name__ == "__main__":
    kmeans_coffee()