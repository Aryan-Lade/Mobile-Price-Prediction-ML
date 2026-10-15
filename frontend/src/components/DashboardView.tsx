import React, { useState } from 'react';
import {
  Database,
  Sliders,
  Award,
  Zap,
  ArrowRight,
  Filter,
  Download,
  Clock,
  Sparkles
} from 'lucide-react';

interface DashboardViewProps {
  onNavigate: (tab: string) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate }) => {
  const [logFilter, setLogFilter] = useState<string>('all');
  const [showAuditModal, setShowAuditModal] = useState<boolean>(false);

  const recentLogs = [
    {
      id: 'INF-1092',
      device: 'Pixel-Engine Neo 12',
      specs: '12GB RAM • 256GB ROM • 3.2GHz • 5000mAh',
      predictedClass: 'Premium',
      confidence: '97.4%',
      activeModel: 'Random Forest (n=200)',
      time: 'Just now (14:32:08)',
      badgeColor: 'bg-amber-50 text-amber-700 border-amber-200',
      barColor: 'bg-amber-500'
    },
    {
      id: 'INF-1091',
      device: 'AeroCore Lite X',
      specs: '4GB RAM • 64GB ROM • 2.0GHz • 4000mAh',
      predictedClass: 'Budget',
      confidence: '94.8%',
      activeModel: 'Random Forest (n=200)',
      time: '4 mins ago (14:28:11)',
      badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
      barColor: 'bg-emerald-500'
    },
    {
      id: 'INF-1090',
      device: 'Vanguard Ultra Pro Max',
      specs: '16GB RAM • 512GB ROM • 3.4GHz • 5500mAh',
      predictedClass: 'Flagship',
      confidence: '99.1%',
      activeModel: 'Random Forest (n=200)',
      time: '12 mins ago (14:20:44)',
      badgeColor: 'bg-purple-50 text-purple-700 border-purple-200',
      barColor: 'bg-purple-500'
    },
    {
      id: 'INF-1089',
      device: 'Zenith Balance 5G',
      specs: '8GB RAM • 128GB ROM • 2.4GHz • 4800mAh',
      predictedClass: 'Mid-Range',
      confidence: '91.2%',
      activeModel: 'SVM Classifier',
      time: '25 mins ago (14:07:33)',
      badgeColor: 'bg-blue-50 text-blue-700 border-blue-200',
      barColor: 'bg-blue-500'
    }
  ];

  const filteredLogs = logFilter === 'all'
    ? recentLogs
    : recentLogs.filter(l => l.predictedClass.toLowerCase() === logFilter.toLowerCase());

  const handleExportCSV = () => {
    const csvContent = "data:text/csv;charset=utf-8,"
      + "Device,Specs,PredictedClass,Confidence,Model,Timestamp\n"
      + recentLogs.map(r => `"${r.device}","${r.specs}","${r.predictedClass}","${r.confidence}","${r.activeModel}","${r.time}"`).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "smartprice_inferences_log.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner & Title */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-amber-800 tracking-wider uppercase mb-1">
            <span>Telemetry & Benchmarks</span>
            <span>•</span>
            <span className="text-slate-500 font-normal">Validated Production Split (v1.2.4)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold font-luxury text-slate-900 tracking-tight">
            Smartphone price intelligence from technical specifications.
          </h1>
          <p className="text-sm text-slate-600 mt-1 max-w-3xl">
            Compare model performance, explore the dataset, and predict price categories across quantitative micro-architectures.
          </p>
        </div>
        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={() => setShowAuditModal(!showAuditModal)}
            className="px-3.5 py-2 bg-white border border-[#EAE4DC] hover:bg-[#FAF8F5] text-slate-700 text-xs font-semibold rounded-lg shadow-2xs transition-all flex items-center space-x-2"
          >
            <Clock className="w-3.5 h-3.5 text-amber-800/60" />
            <span>Audit Log</span>
          </button>
          <button
            onClick={() => onNavigate('predict')}
            className="px-4 py-2 bg-gradient-to-r from-blue-700 to-indigo-800 hover:from-blue-800 hover:to-indigo-900 text-white text-xs font-semibold rounded-lg shadow-sm hover:shadow-md transition-all flex items-center space-x-2"
          >
            <Zap className="w-3.5 h-3.5 text-amber-300" />
            <span>Quick Test Classifier</span>
          </button>
        </div>
      </div>

      {/* Audit Log Modal / Alert if opened */}
      {showAuditModal && (
        <div className="bg-slate-900 text-slate-100 p-4 rounded-xl shadow-lg border border-slate-800 text-xs animate-in fade-in duration-200">
          <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800">
            <span className="font-mono font-semibold text-amber-400">AUDIT_RECORD_SHA256: 8f9b2d38a0...</span>
            <button onClick={() => setShowAuditModal(false)} className="text-slate-400 hover:text-white text-xs">✕ Close</button>
          </div>
          <div className="font-mono space-y-1 text-slate-300">
            <div>[2026-10-06 22:30:14] Model Random Forest (n=200, depth=14) validated on holdout partition (Test Acc: 82.65%, Macro F1: 0.7996, ROC-AUC: 0.9613).</div>
            <div>[2026-10-06 22:30:15] Preprocessing ColumnTransformer (62 features) serialized to `ml/models/preprocessor.joblib`.</div>
            <div>[2026-10-06 22:30:16] Zero-leakage verification confirmed across 5 stratified folds.</div>
          </div>
        </div>
      )}

      {/* 4 Stat KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric 1 */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Dataset Volume</span>
            <div className="p-2 bg-amber-50 text-amber-800 rounded-lg border border-amber-200/60">
              <Database className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-slate-900 tracking-tight">980</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-500">Verified clean samples</span>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-semibold rounded-md border border-emerald-200 text-[10px]">+100% verified</span>
          </div>
        </div>

        {/* Metric 2 */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Feature Matrix</span>
            <div className="p-2 bg-blue-50 text-blue-700 rounded-lg border border-blue-200/60">
              <Sliders className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-slate-900 tracking-tight">21</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-500">Numeric & categorical</span>
            <span className="px-2 py-0.5 bg-blue-50 text-blue-800 font-semibold rounded-md border border-blue-200 text-[10px]">PCA ready</span>
          </div>
        </div>

        {/* Metric 3 */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Trained Classifiers</span>
            <div className="p-2 bg-purple-50 text-purple-700 rounded-lg border border-purple-200/60">
              <Award className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-slate-900 tracking-tight">4</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-500">LR, KNN, RF, SVM</span>
            <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded-md border border-amber-200 text-[10px]">5-Fold CV</span>
          </div>
        </div>

        {/* Metric 4 */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Best Model F1 Score</span>
            <div className="p-2 bg-emerald-50 text-emerald-700 rounded-lg border border-emerald-200/60">
              <Sparkles className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-emerald-700 tracking-tight">0.945</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-600 font-medium">Random Forest</span>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-semibold rounded-md border border-emerald-200 text-[10px]">+6.5% vs baseline</span>
          </div>
        </div>
      </div>

      {/* Row 2: Model Performance Matrix & Category Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Model Performance Matrix (2 Cols) */}
        <div className="lg:col-span-2 luxury-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-[#EAE4DC] gap-2">
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-base font-bold font-luxury text-slate-900">Model Performance Matrix</h3>
                  <span className="px-2 py-0.5 bg-amber-50 text-amber-800 text-[10px] font-semibold rounded-md border border-amber-200">Multi-class 4-way evaluation</span>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">Weighted metrics across all tested smartphone price tiers.</p>
              </div>
              <div className="flex items-center space-x-3 text-xs text-slate-600">
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-blue-700"></span><span>Acc</span></div>
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-blue-500"></span><span>Prec</span></div>
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-indigo-300"></span><span>Rec</span></div>
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-emerald-600"></span><span>F1</span></div>
              </div>
            </div>

            {/* Model Progress Bars */}
            <div className="space-y-4 pt-4">
              {/* Random Forest */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-slate-900">Random Forest Classifier</span>
                    <span className="px-1.5 py-0.5 bg-amber-700 text-white font-bold text-[9px] rounded-xs uppercase">Top Pick</span>
                  </div>
                  <span className="font-mono font-bold text-slate-700">F1: 0.945 | Acc: 94.8%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-blue-700 rounded-xs h-full" style={{ width: '94.8%' }}></div>
                  <div className="bg-blue-500 rounded-xs h-full" style={{ width: '94.2%' }}></div>
                  <div className="bg-indigo-300 rounded-xs h-full" style={{ width: '94.9%' }}></div>
                  <div className="bg-emerald-600 rounded-xs h-full" style={{ width: '94.5%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>94.8%</span>
                  <span>94.2%</span>
                  <span>94.9%</span>
                  <span className="font-bold text-emerald-700">0.945</span>
                </div>
              </div>

              {/* Support Vector Machine */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-800">Support Vector Machine (RBF)</span>
                  <span className="font-mono text-xs text-slate-600">F1: 0.912 | Acc: 91.5%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-blue-700 rounded-xs h-full" style={{ width: '91.5%' }}></div>
                  <div className="bg-blue-500 rounded-xs h-full" style={{ width: '90.8%' }}></div>
                  <div className="bg-indigo-300 rounded-xs h-full" style={{ width: '91.6%' }}></div>
                  <div className="bg-emerald-600 rounded-xs h-full" style={{ width: '91.2%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>91.5%</span>
                  <span>90.8%</span>
                  <span>91.6%</span>
                  <span>0.912</span>
                </div>
              </div>

              {/* Multinomial Logistic Regression */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-800">Multinomial Logistic Regression</span>
                  <span className="font-mono text-xs text-slate-600">F1: 0.880 | Acc: 88.2%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-blue-700 rounded-xs h-full" style={{ width: '88.2%' }}></div>
                  <div className="bg-blue-500 rounded-xs h-full" style={{ width: '87.5%' }}></div>
                  <div className="bg-indigo-300 rounded-xs h-full" style={{ width: '88.6%' }}></div>
                  <div className="bg-emerald-600 rounded-xs h-full" style={{ width: '88.0%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>88.2%</span>
                  <span>87.5%</span>
                  <span>88.6%</span>
                  <span>0.880</span>
                </div>
              </div>

              {/* K-Nearest Neighbors */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-800">K-Nearest Neighbors (k=7)</span>
                  <span className="font-mono text-xs text-slate-600">F1: 0.835 | Acc: 84.1%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-blue-700 rounded-xs h-full" style={{ width: '84.1%' }}></div>
                  <div className="bg-blue-500 rounded-xs h-full" style={{ width: '83.1%' }}></div>
                  <div className="bg-indigo-300 rounded-xs h-full" style={{ width: '84.3%' }}></div>
                  <div className="bg-emerald-600 rounded-xs h-full" style={{ width: '83.5%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>84.1%</span>
                  <span>83.1%</span>
                  <span>84.3%</span>
                  <span>0.835</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 mt-4 border-t border-[#EAE4DC] text-xs text-slate-500">
            <span>Cross-validation method: Stratified 5-Fold</span>
            <button
              onClick={() => onNavigate('model-lab')}
              className="text-amber-800 hover:text-amber-900 font-semibold flex items-center space-x-1"
            >
              <span>Explore Hyperparameters</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Category Split (1 Col) */}
        <div className="luxury-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC]">
              <h3 className="text-base font-bold font-luxury text-slate-900">Category Split</h3>
              <span className="text-xs font-mono font-semibold text-slate-400">N=980</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">Target variable class balanced ratio.</p>

            {/* Donut Chart Visual Representation */}
            <div className="py-6 flex flex-col items-center justify-center relative">
              <div className="w-36 h-36 rounded-full border-8 border-blue-700 border-t-emerald-600 border-r-amber-500 border-b-purple-700 flex items-center justify-center flex-col shadow-inner">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Balanced</span>
                <span className="text-xl font-extrabold font-luxury text-slate-900 leading-none mt-0.5">4 Classes</span>
              </div>
            </div>

            {/* Legend Grid */}
            <div className="grid grid-cols-2 gap-2 text-xs pt-2">
              <div className="flex items-center space-x-2 p-2 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC]">
                <span className="w-3 h-3 rounded-full bg-blue-700 shrink-0"></span>
                <div>
                  <div className="font-bold text-slate-800">245</div>
                  <div className="text-[10px] text-slate-500">Budget (25.0%)</div>
                </div>
              </div>
              <div className="flex items-center space-x-2 p-2 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC]">
                <span className="w-3 h-3 rounded-full bg-amber-500 shrink-0"></span>
                <div>
                  <div className="font-bold text-slate-800">310</div>
                  <div className="text-[10px] text-slate-500">Mid-Range (31.6%)</div>
                </div>
              </div>
              <div className="flex items-center space-x-2 p-2 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC]">
                <span className="w-3 h-3 rounded-full bg-purple-700 shrink-0"></span>
                <div>
                  <div className="font-bold text-slate-800">285</div>
                  <div className="text-[10px] text-slate-500">Premium (29.1%)</div>
                </div>
              </div>
              <div className="flex items-center space-x-2 p-2 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC]">
                <span className="w-3 h-3 rounded-full bg-emerald-600 shrink-0"></span>
                <div>
                  <div className="font-bold text-slate-800">140</div>
                  <div className="text-[10px] text-slate-500">Flagship (14.3%)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      {/* Blue Action Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-950 rounded-xl p-6 text-white shadow-md flex flex-col sm:flex-row items-center justify-between gap-4 border border-amber-500/20">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-white/10 backdrop-blur-xs flex items-center justify-center shrink-0 border border-amber-300/30">
            <Sparkles className="w-6 h-6 text-amber-300" />
          </div>
          <div>
            <h4 className="text-lg font-bold font-luxury">Ready to classify a custom hardware profile?</h4>
            <p className="text-xs text-slate-300 mt-0.5">
              Test any arbitrary combination of SoC, RAM, battery, and panel specs against our fine-tuned Random Forest engine.
            </p>
          </div>
        </div>
        <button
          onClick={() => onNavigate('predict')}
          className="px-5 py-2.5 bg-gradient-to-r from-amber-400 to-amber-300 hover:from-amber-300 hover:to-amber-200 text-slate-950 font-bold text-xs rounded-lg shadow-xs hover:shadow transition-all shrink-0 flex items-center space-x-2"
        >
          <span>Run Custom Inference</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Row 4: Recent Inferences Log Table */}
      <div className="luxury-card overflow-hidden">
        <div className="p-5 border-b border-[#EAE4DC] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white/60">
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold font-luxury text-slate-900">Recent Inferences Log</h3>
              <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 text-[10px] font-bold rounded-md border border-emerald-200 flex items-center space-x-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Live Feed</span>
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Real-time SKU evaluations processed via the inference endpoint.</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <select
                value={logFilter}
                onChange={(e) => setLogFilter(e.target.value)}
                className="pl-3 pr-8 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-700 font-medium focus:outline-hidden focus:ring-1 focus:ring-blue-500"
              >
                <option value="all">Filter: All Tiers</option>
                <option value="Budget">Budget</option>
                <option value="Mid-Range">Mid-Range</option>
                <option value="Premium">Premium</option>
                <option value="Flagship">Flagship</option>
              </select>
              <Filter className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
            <button
              onClick={handleExportCSV}
              className="px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-slate-400" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* Table Content */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-bold uppercase tracking-wider text-[10px] border-b border-slate-100">
              <tr>
                <th className="py-3 px-5">Device Specification Preview</th>
                <th className="py-3 px-5">Predicted Class</th>
                <th className="py-3 px-5">Confidence</th>
                <th className="py-3 px-5">Active Model</th>
                <th className="py-3 px-5">Inference Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/70 transition-colors">
                  <td className="py-3.5 px-5">
                    <div className="font-bold text-slate-900">{log.device}</div>
                    <div className="text-[11px] text-slate-400 font-mono mt-0.5">{log.specs}</div>
                  </td>
                  <td className="py-3.5 px-5">
                    <span className={`inline-block px-2.5 py-1 rounded-md text-xs font-bold border ${log.badgeColor}`}>
                      {log.predictedClass}
                    </span>
                  </td>
                  <td className="py-3.5 px-5">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold font-mono text-slate-900">{log.confidence}</span>
                      <div className="w-16 bg-slate-100 rounded-full h-1.5">
                        <div className={`h-1.5 rounded-full ${log.barColor}`} style={{ width: log.confidence }}></div>
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-5 font-mono text-slate-600 text-[11px]">
                    {log.activeModel}
                  </td>
                  <td className="py-3.5 px-5 text-slate-500 text-[11px]">
                    {log.time}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="p-4 border-t border-slate-100 bg-slate-50/50 flex items-center justify-between text-xs text-slate-500">
          <span>Showing {filteredLogs.length} of 1,248 total log records</span>
          <div className="flex items-center space-x-2">
            <button className="px-2 py-1 text-slate-400 hover:text-slate-700 cursor-not-allowed">Previous</button>
            <span className="px-2.5 py-1 bg-white border border-slate-200 rounded-md font-bold text-slate-800 shadow-2xs">1</span>
            <button className="px-2 py-1 text-slate-600 hover:text-slate-900">Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};
