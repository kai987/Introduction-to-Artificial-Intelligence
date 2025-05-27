import React, { useState } from 'react';

const KMeansCoffee = () => {
  const [results, setResults] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [showNormalization, setShowNormalization] = useState(false);

  // 元のデータ（講義の課題3と同じ）
  const rawData = [
    { name: 'coffee1', bitterness: 73, acidity: 6 },
    { name: 'coffee2', bitterness: 60, acidity: 6 },
    { name: 'coffee3', bitterness: 48, acidity: 5 },
    { name: 'coffee4', bitterness: 65, acidity: 7 },
    { name: 'coffee5', bitterness: 30, acidity: 7 },
    { name: 'coffee6', bitterness: 78, acidity: 4 },
    { name: 'coffee7', bitterness: 51, acidity: 5 }
  ];

  // Min-Max正規化（講義の例に従って）
  const normalizeData = (data) => {
    const bitterness = data.map(d => d.bitterness);
    const acidity = data.map(d => d.acidity);
    
    const bitternessMax = Math.max(...bitterness);
    const bitternessMin = Math.min(...bitterness);
    const acidityMax = Math.max(...acidity);
    const acidityMin = Math.min(...acidity);
    
    const bitternessRange = bitternessMax - bitternessMin;
    const acidityRange = acidityMax - acidityMin;

    return {
      normalizedData: data.map(d => ({
        name: d.name,
        bitterness: (d.bitterness - bitternessMin) / bitternessRange,
        acidity: (d.acidity - acidityMin) / acidityRange,
        originalBitterness: d.bitterness,
        originalAcidity: d.acidity
      })),
      stats: {
        bitterness: { min: bitternessMin, max: bitternessMax, range: bitternessRange },
        acidity: { min: acidityMin, max: acidityMax, range: acidityRange }
      }
    };
  };

  // ユークリッド距離の計算（講義の式に従って）
  const euclideanDistance = (p1, p2) => {
    return Math.sqrt(Math.pow(p1.bitterness - p2.bitterness, 2) + Math.pow(p1.acidity - p2.acidity, 2));
  };

  // 重心の計算（講義の式：平均値）
  const calculateCentroid = (points) => {
    if (points.length === 0) return { bitterness: 0, acidity: 0 };
    
    const sumBitterness = points.reduce((sum, p) => sum + p.bitterness, 0);
    const sumAcidity = points.reduce((sum, p) => sum + p.acidity, 0);
    
    return {
      bitterness: sumBitterness / points.length,
      acidity: sumAcidity / points.length
    };
  };

  // K平均法の実行（講義の手順に従って）
  const runKMeans = () => {
    setIsRunning(true);
    setResults([]);
    
    const { normalizedData, stats } = normalizeData(rawData);
    const k = 2; // 2つのクラスターに分ける
    const maxIterations = 10;
    
    // 初期中心点を設定（講義の例：center0, center1のように）
    let centroids = [
      { bitterness: 0.5, acidity: 0.25 }, // center0相当
      { bitterness: 0.75, acidity: 0.95 }  // center1相当
    ];
    
    const iterationResults = [];
    
    // 正規化情報を追加
    iterationResults.push({
      round: -1,
      type: 'normalization',
      normalizedData: [...normalizedData],
      stats: stats,
      message: "データの正規化完了"
    });
    
    // 初期状態を記録
    iterationResults.push({
      round: 0,
      type: 'initial',
      centroids: [...centroids],
      clusters: [[], []],
      converged: false,
      message: "初期中心点設定",
      distances: []
    });

    for (let iteration = 1; iteration <= maxIterations; iteration++) {
      // ステップ3: 各データポイントを最も近い中心点に割り当て
      const clusters = [[], []];
      const distances = [];
      
      normalizedData.forEach(point => {
        const dist0 = euclideanDistance(point, centroids[0]);
        const dist1 = euclideanDistance(point, centroids[1]);
        
        distances.push({
          point: point.name,
          dist0: dist0,
          dist1: dist1,
          assigned: dist0 < dist1 ? 0 : 1
        });
        
        const closestCentroid = dist0 < dist1 ? 0 : 1;
        clusters[closestCentroid].push(point);
      });
      
      // ステップ4: 新しい中心点を計算（重心）
      const newCentroids = clusters.map(cluster => calculateCentroid(cluster));
      
      // 収束判定
      const converged = centroids.every((centroid, i) => 
        Math.abs(centroid.bitterness - newCentroids[i].bitterness) < 0.001 &&
        Math.abs(centroid.acidity - newCentroids[i].acidity) < 0.001
      );
      
      iterationResults.push({
        round: iteration,
        type: 'iteration',
        centroids: [...newCentroids],
        oldCentroids: [...centroids],
        clusters: clusters.map(cluster => [...cluster]),
        distances: [...distances],
        converged,
        message: converged ? "収束しました" : "継続中"
      });
      
      centroids = newCentroids;
      
      if (converged) break;
    }
    
    setTimeout(() => {
      setResults(iterationResults);
      setIsRunning(false);
    }, 1000);
  };

  return (
    <div className="max-w-7xl mx-auto p-6 bg-white">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-center mb-4 text-blue-800">
          🎓 K平均法 - 百万遍コーヒー店の課題
        </h1>
        <p className="text-center text-gray-600 mb-4">
          京都情報大学院大学 人工知能概論第5回 - 教師なし学習
        </p>
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-semibold text-blue-800 mb-2">📋 課題内容</h3>
          <p className="text-gray-700">
            K平均法を使って以下のコーヒーを2つのグループ（クラスター）に分けなさい。<br/>
            データは、規格化すること！
          </p>
        </div>
      </div>

      {/* 元データ表示 */}
      <div className="mb-8 bg-amber-50 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-4 text-amber-800">📊 元データ</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-amber-200">
            <thead>
              <tr className="bg-amber-100">
                <th className="border border-amber-200 px-4 py-2">コーヒー</th>
                <th className="border border-amber-200 px-4 py-2">苦味</th>
                <th className="border border-amber-200 px-4 py-2">酸味</th>
              </tr>
            </thead>
            <tbody>
              {rawData.map((coffee, i) => (
                <tr key={i} className="hover:bg-amber-25">
                  <td className="border border-amber-200 px-4 py-2 font-medium">{coffee.name}</td>
                  <td className="border border-amber-200 px-4 py-2 text-center">{coffee.bitterness}</td>
                  <td className="border border-amber-200 px-4 py-2 text-center">{coffee.acidity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* K平均法の手順説明 */}
      <div className="mb-8 bg-blue-50 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-4 text-blue-800">🔄 K平均法の手順</h2>
        <ol className="list-decimal list-inside space-y-2 text-gray-700">
          <li><strong>データの正規化:</strong> Min-Max正規化を適用（講義の例に従って）</li>
          <li><strong>クラスター数の設定:</strong> K=2（2つのグループに分ける）</li>
          <li><strong>初期中心点の設定:</strong> center0=[0.5, 0.25], center1=[0.75, 0.95]</li>
          <li><strong>距離計算:</strong> 各データポイントと中心点のユークリッド距離を計算</li>
          <li><strong>クラスター割り当て:</strong> 最も近い中心点のクラスターに割り当て</li>
          <li><strong>重心の再計算:</strong> 各クラスターの重心を新しい中心点とする</li>
          <li><strong>繰り返し:</strong> 収束するまで手順4-6を繰り返す</li>
        </ol>
      </div>

      {/* 実行ボタン */}
      <div className="text-center mb-8">
        <button
          onClick={runKMeans}
          disabled={isRunning}
          className={`px-8 py-3 rounded-lg text-white font-semibold text-lg transition-all mr-4 ${
            isRunning 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
          }`}
        >
          {isRunning ? '⏳ 実行中...' : '🚀 K平均法を実行'}
        </button>
        
        <button
          onClick={() => setShowNormalization(!showNormalization)}
          className="px-6 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 transition-all"
        >
          {showNormalization ? '正規化を隠す' : '正規化を表示'}
        </button>
      </div>

      {/* 結果表示 */}
      {results.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-center text-blue-800 mb-6">
            📈 K平均法の実行結果
          </h2>
          
          {results.map((result, i) => (
            <div key={i}>
              {/* 正規化結果 */}
              {result.type === 'normalization' && showNormalization && (
                <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-400 mb-6">
                  <h3 className="text-xl font-semibold text-green-800 mb-4">📐 データの正規化</h3>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold mb-2">正規化前後の比較</h4>
                      <div className="overflow-x-auto">
                        <table className="w-full border-collapse border border-green-200 text-sm">
                          <thead>
                            <tr className="bg-green-100">
                              <th className="border border-green-200 px-2 py-1">コーヒー</th>
                              <th className="border border-green-200 px-2 py-1">元苦味</th>
                              <th className="border border-green-200 px-2 py-1">正規化苦味</th>
                              <th className="border border-green-200 px-2 py-1">元酸味</th>
                              <th className="border border-green-200 px-2 py-1">正規化酸味</th>
                            </tr>
                          </thead>
                          <tbody>
                            {result.normalizedData.map((coffee, j) => (
                              <tr key={j}>
                                <td className="border border-green-200 px-2 py-1">{coffee.name}</td>
                                <td className="border border-green-200 px-2 py-1 text-center">{coffee.originalBitterness}</td>
                                <td className="border border-green-200 px-2 py-1 text-center">{coffee.bitterness.toFixed(3)}</td>
                                <td className="border border-green-200 px-2 py-1 text-center">{coffee.originalAcidity}</td>
                                <td className="border border-green-200 px-2 py-1 text-center">{coffee.acidity.toFixed(3)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">正規化パラメータ</h4>
                      <div className="bg-white p-4 rounded border text-sm">
                        <p><strong>苦味:</strong> Min={result.stats.bitterness.min}, Max={result.stats.bitterness.max}</p>
                        <p><strong>酸味:</strong> Min={result.stats.acidity.min}, Max={result.stats.acidity.max}</p>
                        <p className="mt-2 text-xs text-gray-600">
                          正規化式: (値 - Min) / (Max - Min)
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 各ラウンドの結果 */}
              {result.type !== 'normalization' && (
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border-l-4 border-blue-400">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-semibold text-gray-800">
                      {result.round === 0 ? '🎯 初期状態' : `🔄 ラウンド ${result.round}`}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      result.converged ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {result.message}
                    </span>
                  </div>
                  
                  {/* 中心点情報 */}
                  {result.round > 0 && (
                    <div className="mb-4 bg-white p-4 rounded-lg">
                      <h4 className="font-semibold mb-2">📍 中心点の更新</h4>
                      <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <p><strong>前回の中心点:</strong></p>
                          <p>Center0: ({result.oldCentroids[0].bitterness.toFixed(3)}, {result.oldCentroids[0].acidity.toFixed(3)})</p>
                          <p>Center1: ({result.oldCentroids[1].bitterness.toFixed(3)}, {result.oldCentroids[1].acidity.toFixed(3)})</p>
                        </div>
                        <div>
                          <p><strong>新しい中心点:</strong></p>
                          <p>Center0: ({result.centroids[0].bitterness.toFixed(3)}, {result.centroids[0].acidity.toFixed(3)})</p>
                          <p>Center1: ({result.centroids[1].bitterness.toFixed(3)}, {result.centroids[1].acidity.toFixed(3)})</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* 距離計算詳細 */}
                  {result.distances && result.distances.length > 0 && (
                    <div className="mb-4 bg-white p-4 rounded-lg">
                      <h4 className="font-semibold mb-2">📏 距離計算の詳細</h4>
                      <div className="overflow-x-auto">
                        <table className="w-full border-collapse border border-gray-200 text-sm">
                          <thead>
                            <tr className="bg-gray-100">
                              <th className="border border-gray-200 px-2 py-1">コーヒー</th>
                              <th className="border border-gray-200 px-2 py-1">Center0への距離</th>
                              <th className="border border-gray-200 px-2 py-1">Center1への距離</th>
                              <th className="border border-gray-200 px-2 py-1">割り当て</th>
                            </tr>
                          </thead>
                          <tbody>
                            {result.distances.map((dist, j) => (
                              <tr key={j} className={dist.assigned === 0 ? 'bg-blue-25' : 'bg-green-25'}>
                                <td className="border border-gray-200 px-2 py-1">{dist.point}</td>
                                <td className="border border-gray-200 px-2 py-1 text-center">{dist.dist0.toFixed(3)}</td>
                                <td className="border border-gray-200 px-2 py-1 text-center">{dist.dist1.toFixed(3)}</td>
                                <td className="border border-gray-200 px-2 py-1 text-center">
                                  <span className={`px-2 py-1 rounded text-xs ${
                                    dist.assigned === 0 ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                                  }`}>
                                    クラスター{dist.assigned + 1}
                                  </span>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                  
                  {/* クラスター結果 */}
                  <div className="grid md:grid-cols-2 gap-6">
                    {result.clusters.map((cluster, clusterIndex) => (
                      <div key={clusterIndex} className="bg-white p-4 rounded-lg shadow-sm">
                        <h4 className={`font-semibold mb-3 text-lg ${
                          clusterIndex === 0 ? 'text-blue-700' : 'text-green-700'
                        }`}>
                          {clusterIndex === 0 ? '🔵' : '🟢'} クラスター {clusterIndex + 1}
                          <span className="ml-2 text-sm text-gray-500">
                            ({cluster.length}個)
                          </span>
                        </h4>
                        
                        {cluster.length > 0 ? (
                          <div className="space-y-2">
                            {cluster.map((coffee, coffeeIndex) => (
                              <div key={coffeeIndex} className="flex justify-between items-center p-2 bg-gray-50 rounded text-sm">
                                <span className="font-medium">{coffee.name}</span>
                                <span className="text-gray-600">
                                  苦味:{coffee.originalBitterness} 酸味:{coffee.originalAcidity}
                                </span>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-gray-500 italic">このクラスターは空です</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default KMeansCoffee;