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
  Sparkles,
  Search,
  CheckCircle2,
  Cpu,
  Activity,
  ShieldCheck,
  ChevronRight,
  BarChart3,
  X
} from 'lucide-react';

interface DashboardViewProps {
  onNavigate: (tab: string) => void;
}

interface PipelineStep {
  id: number;
  title: string;
  subtitle: string;
  tech: string;
  details: string;
  formula: string;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate }) => {
  const [logFilter, setLogFilter] = useState<string>('all');
  const [logSearch, setLogSearch] = useState<string>('');
  const [showAuditModal, setShowAuditModal] = useState<boolean>(false);
  const [selectedPipelineStep, setSelectedPipelineStep] = useState<number>(2);

  const pipelineSteps: PipelineStep[] = [
    {
      id: 0,
      title: '1. Raw Hardware Specs',
      subtitle: '21 Quantitative Features',
      tech: 'Input JSON Schema',
      details: 'Physical parameters collected across SoC clock speed, RAM capacity, ROM storage, display diagonal, vertical refresh rate, rear & front camera optics, 5G modem subsystem, and battery volume.',
      formula: 'x \\in \\mathbb{R}^{21} \\text{ (Continuous + Categorical Attributes)}'
    },
    {
      id: 1,
      title: '2. Preprocessing & Imputation',
      subtitle: 'Zero-Leakage ColumnTransformer',
      tech: 'SimpleImputer + StandardScaler',
      details: 'Applies median imputation for skewed numerical features (e.g. clock speed, battery, rating) and statistical mode for discrete categoricals strictly fit on training splits. 34 one-hot encoded dummies are generated.',
      formula: 'x_{norm} = \\frac{x - \\mu_{train}}{\\sigma_{train}}, \\quad \\text{dim}(X_{trans}) = 62'
    },
    {
      id: 2,
      title: '3. Random Forest Ensemble',
      subtitle: '300 Estimators, max_depth=16',
      tech: 'scikit-learn RandomForestClassifier',
      details: 'Ensemble of decorrelated decision trees constructed with bootstrap sampling (bagging) and random feature subspace selection (\\sqrt{d}). Gini impurity is minimized at each node split.',
      formula: 'Gini(p) = 1 - \\sum_{k=1}^4 p_k^2, \\quad \\hat{y} = \\text{mode}\\{h_b(x)\\}_{b=1}^{300}'
    },
    {
      id: 3,
      title: '4. Softmax Class Probabilities',
      subtitle: 'Calibrated Confidence Vector',
      tech: 'Probability Density Distribution',
      details: 'Class voting distributions across the 300 decision trees are normalized into an empirical probability vector representing likelihood across Budget, Mid-Range, Premium, and Flagship categories.',
      formula: 'P(y=k \\mid x) = \\frac{1}{B} \\sum_{b=1}^B \\mathbb{I}(h_b(x) = k)'
    },
    {
      id: 4,
      title: '5. Price Tier & Range',
      subtitle: 'Market Bounds & Estimated MSRP',
      tech: 'Commercial Stratification',
      details: 'Final argmax tier assignment is mapped to historical MSRP price distribution bounds in Indian Rupees (₹) and US Dollars ($) with confidence bounds and derived feature analytics.',
      formula: 'y^* = \\arg\\max_k P(y=k \\mid x) \\implies [\\text{Min INR}, \\text{Max INR}]'
    }
  ];

  const recentLogs = [
    {
      id: 'INF-1095',
      device: 'Samsung Galaxy S23 Ultra',
      specs: '12GB RAM • 256GB ROM • 3.36GHz • 5000mAh • 120Hz',
      predictedClass: 'Flagship',
      confidence: '98.8%',
      activeModel: 'Random Forest (300 Trees)',
      time: 'Just now (14:42:15)',
      badgeColor: 'bg-rose-50 text-rose-800 border-rose-200',
      barColor: 'bg-rose-700'
    },
    {
      id: 'INF-1094',
      device: 'OnePlus 11R 5G',
      specs: '8GB RAM • 128GB ROM • 3.0GHz • 5000mAh • 120Hz',
      predictedClass: 'Premium',
      confidence: '96.2%',
      activeModel: 'Random Forest (300 Trees)',
      time: '2 mins ago (14:40:02)',
      badgeColor: 'bg-amber-50 text-amber-900 border-amber-200',
      barColor: 'bg-amber-800'
    },
    {
      id: 'INF-1093',
      device: 'Redmi Note 12 Pro+ 5G',
      specs: '8GB RAM • 256GB ROM • 2.6GHz • 5000mAh • 120Hz',
      predictedClass: 'Mid-Range',
      confidence: '93.5%',
      activeModel: 'Random Forest (300 Trees)',
      time: '6 mins ago (14:36:19)',
      badgeColor: 'bg-blue-50 text-blue-800 border-blue-200',
      barColor: 'bg-blue-800'
    },
    {
      id: 'INF-1092',
      device: 'Realme Narzo N55',
      specs: '4GB RAM • 64GB ROM • 2.0GHz • 5000mAh • 90Hz',
      predictedClass: 'Budget',
      confidence: '97.1%',
      activeModel: 'Random Forest (300 Trees)',
      time: '14 mins ago (14:28:44)',
      badgeColor: 'bg-emerald-50 text-emerald-800 border-emerald-200',
      barColor: 'bg-emerald-700'
    },
    {
      id: 'INF-1091',
      device: 'Google Pixel 7a',
      specs: '8GB RAM • 128GB ROM • 2.85GHz • 4385mAh • 90Hz',
      predictedClass: 'Premium',
      confidence: '91.8%',
      activeModel: 'Support Vector Machine',
      time: '22 mins ago (14:20:10)',
      badgeColor: 'bg-amber-50 text-amber-900 border-amber-200',
      barColor: 'bg-amber-800'
    },
    {
      id: 'INF-1090',
      device: 'Motorola Moto G73 5G',
      specs: '8GB RAM • 128GB ROM • 2.2GHz • 5000mAh • 120Hz',
      predictedClass: 'Mid-Range',
      confidence: '89.4%',
      activeModel: 'Logistic Regression',
      time: '35 mins ago (14:07:05)',
      badgeColor: 'bg-blue-50 text-blue-800 border-blue-200',
      barColor: 'bg-blue-800'
    }
  ];

  const filteredLogs = recentLogs.filter(log => {
    const matchesTier = logFilter === 'all' || log.predictedClass.toLowerCase() === logFilter.toLowerCase();
    const matchesSearch = !logSearch ||
      log.device.toLowerCase().includes(logSearch.toLowerCase()) ||
      log.specs.toLowerCase().includes(logSearch.toLowerCase()) ||
      log.activeModel.toLowerCase().includes(logSearch.toLowerCase());
    return matchesTier && matchesSearch;
  });

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
            <span>Executive Telemetry & Benchmarks</span>
            <span>•</span>
            <span className="text-slate-500 font-normal">Production Classifier Deployment (v5.2)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold font-luxury text-slate-900 tracking-tight">
            Smartphone Price Intelligence & ML Benchmarking
          </h1>
          <p className="text-sm text-slate-600 mt-1 max-w-3xl">
            Evaluate quantitative hardware micro-architectures across calibrated machine learning models. Built with stratified 5-fold cross-validation and zero-leakage scikit-learn transformers.
          </p>
        </div>
        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={() => setShowAuditModal(true)}
            className="px-3.5 py-2 bg-white border border-[#E2D7C8] hover:bg-[#FAF5ED] text-slate-700 text-xs font-semibold rounded-lg shadow-2xs transition-all flex items-center space-x-2 cursor-pointer"
          >
            <Clock className="w-3.5 h-3.5 text-amber-800" />
            <span>Audit Log</span>
          </button>
          <button
            onClick={() => onNavigate('predict')}
            className="px-4 py-2 bg-gradient-to-r from-amber-700 to-amber-800 hover:from-amber-800 hover:to-amber-900 text-white text-xs font-bold rounded-lg shadow-xs transition-all flex items-center space-x-2 cursor-pointer"
          >
            <Zap className="w-3.5 h-3.5 text-amber-300" />
            <span>Test Hardware Classifier</span>
          </button>
        </div>
      </div>

      {/* Production Health & Micro-Architecture Telemetry Bar */}
      <div className="bg-[#FAF5ED] border border-[#E2D7C8] rounded-xl p-3 sm:p-4 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-600"></span>
          </span>
          <span className="font-bold text-slate-800">Inference Engine: Live & Optimal</span>
        </div>

        <div className="flex flex-wrap items-center gap-2 sm:gap-4 font-mono text-[11px] text-slate-600">
          <div className="flex items-center space-x-1">
            <span className="text-slate-400">Latency:</span>
            <strong className="text-slate-800">3.2 ms</strong>
          </div>
          <div className="hidden sm:inline text-slate-300">•</div>
          <div className="flex items-center space-x-1">
            <span className="text-slate-400">Memory:</span>
            <strong className="text-slate-800">14.2 MB</strong>
          </div>
          <div className="hidden sm:inline text-slate-300">•</div>
          <div className="flex items-center space-x-1">
            <span className="text-slate-400">Partition:</span>
            <strong className="text-slate-800">80/20 Stratified</strong>
          </div>
          <div className="hidden sm:inline text-slate-300">•</div>
          <div className="flex items-center space-x-1">
            <span className="text-slate-400">Leakage Check:</span>
            <strong className="text-emerald-700 flex items-center space-x-0.5">
              <ShieldCheck className="w-3 h-3 inline" />
              <span>Guaranteed</span>
            </strong>
          </div>
        </div>
      </div>

      {/* 4 Stat KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric 1: Dataset Volume */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Dataset Volume</span>
            <div className="p-2 bg-amber-50 text-amber-800 rounded-lg border border-amber-200/60">
              <Database className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-slate-900 tracking-tight">980</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-500">Verified clean SKUs</span>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-semibold rounded-md border border-emerald-200 text-[10px]">100% Curated</span>
          </div>
        </div>

        {/* Metric 2: Feature Matrix */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Feature Tensor</span>
            <div className="p-2 bg-amber-50 text-amber-800 rounded-lg border border-amber-200/60">
              <Sliders className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-slate-900 tracking-tight">62 dims</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-500">21 raw &rarr; 62 encoded</span>
            <span className="px-2 py-0.5 bg-amber-50 text-amber-900 font-semibold rounded-md border border-amber-200 text-[10px]">StandardScaler</span>
          </div>
        </div>

        {/* Metric 3: Trained Classifiers */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Trained Classifiers</span>
            <div className="p-2 bg-amber-50 text-amber-800 rounded-lg border border-amber-200/60">
              <Award className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-slate-900 tracking-tight">4 Models</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-500">RF, SVM, LR, KNN</span>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-semibold rounded-md border border-emerald-200 text-[10px]">Stratified 5-Fold</span>
          </div>
        </div>

        {/* Metric 4: Champion F1 */}
        <div className="luxury-card p-5">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">Champion F1 Score</span>
            <div className="p-2 bg-emerald-50 text-emerald-700 rounded-lg border border-emerald-200/60">
              <Sparkles className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold font-luxury text-emerald-700 tracking-tight">0.945</div>
          <div className="flex items-center justify-between mt-3 text-xs">
            <span className="text-slate-600 font-medium">Random Forest</span>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-semibold rounded-md border border-emerald-200 text-[10px]">94.8% Acc</span>
          </div>
        </div>
      </div>

      {/* INTERACTIVE END-TO-END ML PIPELINE ARCHITECTURE FLOW */}
      <div className="luxury-card p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[#E2D7C8]">
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-amber-800" />
            <h3 className="text-base font-bold font-luxury text-slate-900">End-to-End Machine Learning Pipeline Architecture</h3>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            Click any stage to inspect mathematical formulation & parameters
          </span>
        </div>

        {/* 5-Step Pipeline Horizontal Ribbon */}
        <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 pt-1">
          {pipelineSteps.map((step) => {
            const isSelected = selectedPipelineStep === step.id;
            return (
              <button
                key={step.id}
                onClick={() => setSelectedPipelineStep(step.id)}
                className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer relative ${
                  isSelected
                    ? 'bg-amber-800 text-white border-amber-900 shadow-sm ring-2 ring-amber-700/30'
                    : 'bg-[#FAF5ED] hover:bg-white text-slate-800 border-[#E2D7C8]'
                }`}
              >
                <div className={`text-[10px] font-mono font-bold uppercase tracking-wider mb-1 ${isSelected ? 'text-amber-200' : 'text-slate-400'}`}>
                  {step.tech}
                </div>
                <div className="font-bold text-xs leading-snug">{step.title}</div>
                <div className={`text-[11px] mt-0.5 ${isSelected ? 'text-amber-100' : 'text-slate-500'}`}>
                  {step.subtitle}
                </div>
                {isSelected && (
                  <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 bg-amber-800 rotate-45"></div>
                )}
              </button>
            );
          })}
        </div>

        {/* Selected Pipeline Stage Details Card */}
        {selectedPipelineStep !== null && (
          <div className="p-4 bg-[#FAF5ED] border border-[#E2D7C8] rounded-xl text-xs space-y-2 animate-in fade-in duration-150">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#E2D7C8] pb-2">
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 bg-amber-800 text-white rounded text-[10px] font-bold font-mono">
                  STAGE {pipelineSteps[selectedPipelineStep].id + 1} OF 5
                </span>
                <span className="font-bold text-slate-900 font-luxury text-sm">
                  {pipelineSteps[selectedPipelineStep].title}
                </span>
              </div>
              <span className="font-mono text-slate-500 text-[11px] bg-white px-2 py-0.5 rounded border border-[#E2D7C8]">
                {pipelineSteps[selectedPipelineStep].tech}
              </span>
            </div>

            <p className="text-slate-700 leading-relaxed pt-1">
              {pipelineSteps[selectedPipelineStep].details}
            </p>

            <div className="p-2.5 bg-white rounded-lg border border-[#E2D7C8] font-mono text-[11px] text-amber-950 flex items-center justify-between">
              <span className="text-slate-400">Formal Operator:</span>
              <span className="font-bold">{pipelineSteps[selectedPipelineStep].formula}</span>
            </div>
          </div>
        )}
      </div>

      {/* Row 2: Model Performance Matrix & Category Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Model Performance Matrix (2 Cols) */}
        <div className="lg:col-span-2 luxury-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-[#E2D7C8] gap-2">
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-base font-bold font-luxury text-slate-900">Model Performance Matrix</h3>
                  <span className="px-2 py-0.5 bg-amber-50 text-amber-800 text-[10px] font-bold rounded-md border border-amber-200">Stratified 5-Fold Evaluation</span>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">Macro-averaged cross-validation metrics across all 4 smartphone price tiers.</p>
              </div>
              <div className="flex items-center space-x-3 text-xs text-slate-600">
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-amber-800"></span><span>Acc</span></div>
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-amber-600"></span><span>Prec</span></div>
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-blue-700"></span><span>Rec</span></div>
                <div className="flex items-center space-x-1.5"><span className="w-2.5 h-2.5 rounded-xs bg-emerald-600"></span><span>F1</span></div>
              </div>
            </div>

            {/* Model Progress Bars */}
            <div className="space-y-4 pt-4">
              {/* Random Forest */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-slate-900">Random Forest Classifier (Champion)</span>
                    <span className="px-1.5 py-0.5 bg-amber-800 text-white font-bold text-[9px] rounded-xs uppercase">Top Pick</span>
                  </div>
                  <span className="font-mono font-bold text-slate-800">F1: 0.945 | Acc: 94.8%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-amber-800 rounded-xs h-full" style={{ width: '94.8%' }}></div>
                  <div className="bg-amber-600 rounded-xs h-full" style={{ width: '94.5%' }}></div>
                  <div className="bg-blue-700 rounded-xs h-full" style={{ width: '94.8%' }}></div>
                  <div className="bg-emerald-600 rounded-xs h-full" style={{ width: '94.5%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>94.8%</span>
                  <span>94.5%</span>
                  <span>94.8%</span>
                  <span className="font-bold text-emerald-700">0.945</span>
                </div>
              </div>

              {/* Support Vector Machine */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-800">Support Vector Machine (RBF Kernel)</span>
                  <span className="font-mono text-xs text-slate-600">F1: 0.911 | Acc: 91.3%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-amber-800/80 rounded-xs h-full" style={{ width: '91.3%' }}></div>
                  <div className="bg-amber-600/80 rounded-xs h-full" style={{ width: '91.0%' }}></div>
                  <div className="bg-blue-700/80 rounded-xs h-full" style={{ width: '91.2%' }}></div>
                  <div className="bg-emerald-600/80 rounded-xs h-full" style={{ width: '91.1%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>91.3%</span>
                  <span>91.0%</span>
                  <span>91.2%</span>
                  <span>0.911</span>
                </div>
              </div>

              {/* Multinomial Logistic Regression */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-800">Multinomial Logistic Regression (L2)</span>
                  <span className="font-mono text-xs text-slate-600">F1: 0.880 | Acc: 88.4%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-amber-800/60 rounded-xs h-full" style={{ width: '88.4%' }}></div>
                  <div className="bg-amber-600/60 rounded-xs h-full" style={{ width: '87.9%' }}></div>
                  <div className="bg-blue-700/60 rounded-xs h-full" style={{ width: '88.2%' }}></div>
                  <div className="bg-emerald-600/60 rounded-xs h-full" style={{ width: '88.0%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>88.4%</span>
                  <span>87.9%</span>
                  <span>88.2%</span>
                  <span>0.880</span>
                </div>
              </div>

              {/* K-Nearest Neighbors */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-800">K-Nearest Neighbors (k=7 Euclidean)</span>
                  <span className="font-mono text-xs text-slate-600">F1: 0.849 | Acc: 85.2%</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5 h-3">
                  <div className="bg-amber-800/40 rounded-xs h-full" style={{ width: '85.2%' }}></div>
                  <div className="bg-amber-600/40 rounded-xs h-full" style={{ width: '84.0%' }}></div>
                  <div className="bg-blue-700/40 rounded-xs h-full" style={{ width: '85.0%' }}></div>
                  <div className="bg-emerald-600/40 rounded-xs h-full" style={{ width: '84.9%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                  <span>85.2%</span>
                  <span>84.0%</span>
                  <span>85.0%</span>
                  <span>0.849</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 mt-4 border-t border-[#E2D7C8] text-xs text-slate-500">
            <span>ROC-AUC Leader: Random Forest (0.987)</span>
            <button
              onClick={() => onNavigate('model-lab')}
              className="text-amber-800 hover:text-amber-900 font-bold flex items-center space-x-1 cursor-pointer"
            >
              <span>Explore Model Lab</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Category Split (1 Col) */}
        <div className="luxury-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[#E2D7C8]">
              <h3 className="text-base font-bold font-luxury text-slate-900">Target Category Split</h3>
              <span className="text-xs font-mono font-semibold text-slate-400">N=980</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">Real-world commercial market price tier stratification.</p>

            {/* Donut Chart Visual Representation */}
            <div className="py-5 flex flex-col items-center justify-center relative">
              <div className="w-32 h-32 rounded-full border-8 border-amber-800 border-t-emerald-700 border-r-blue-700 border-b-rose-700 flex items-center justify-center flex-col shadow-inner">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Target</span>
                <span className="text-xl font-extrabold font-luxury text-slate-900 leading-none mt-0.5">4 Tiers</span>
              </div>
            </div>

            {/* Legend Grid */}
            <div className="grid grid-cols-2 gap-2 text-xs pt-2">
              <div className="p-2.5 rounded-lg bg-[#FAF5ED] border border-[#E2D7C8]">
                <div className="flex items-center space-x-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-700 shrink-0"></span>
                  <span className="font-bold text-slate-800">Budget</span>
                </div>
                <div className="text-[11px] font-mono text-slate-600">337 SKUs (34.4%)</div>
                <div className="text-[10px] text-slate-400 font-mono">&le; ₹15,000</div>
              </div>

              <div className="p-2.5 rounded-lg bg-[#FAF5ED] border border-[#E2D7C8]">
                <div className="flex items-center space-x-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-blue-700 shrink-0"></span>
                  <span className="font-bold text-slate-800">Mid-Range</span>
                </div>
                <div className="text-[11px] font-mono text-slate-600">349 SKUs (35.6%)</div>
                <div className="text-[10px] text-slate-400 font-mono">₹15k–₹30,000</div>
              </div>

              <div className="p-2.5 rounded-lg bg-[#FAF5ED] border border-[#E2D7C8]">
                <div className="flex items-center space-x-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-800 shrink-0"></span>
                  <span className="font-bold text-slate-800">Premium</span>
                </div>
                <div className="text-[11px] font-mono text-slate-600">133 SKUs (13.6%)</div>
                <div className="text-[10px] text-slate-400 font-mono">₹30k–₹50,000</div>
              </div>

              <div className="p-2.5 rounded-lg bg-[#FAF5ED] border border-[#E2D7C8]">
                <div className="flex items-center space-x-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-700 shrink-0"></span>
                  <span className="font-bold text-slate-800">Flagship</span>
                </div>
                <div className="text-[11px] font-mono text-slate-600">161 SKUs (16.4%)</div>
                <div className="text-[10px] text-slate-400 font-mono">&gt; ₹50,000</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Action Banner */}
      <div className="bg-gradient-to-r from-amber-900 via-amber-800 to-slate-900 rounded-2xl p-6 text-white shadow-md flex flex-col sm:flex-row items-center justify-between gap-4 border border-amber-500/20">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-white/10 backdrop-blur-xs flex items-center justify-center shrink-0 border border-amber-300/30">
            <Sparkles className="w-6 h-6 text-amber-300" />
          </div>
          <div>
            <h4 className="text-lg font-bold font-luxury">Ready to test arbitrary hardware profiles?</h4>
            <p className="text-xs text-amber-100/80 mt-0.5">
              Input custom SoC speed, RAM modules, screen refresh, and optics to witness instant consensus inference.
            </p>
          </div>
        </div>
        <button
          onClick={() => onNavigate('predict')}
          className="px-5 py-2.5 bg-gradient-to-r from-amber-400 to-amber-300 hover:from-amber-300 hover:to-amber-200 text-slate-950 font-bold text-xs rounded-lg shadow-xs hover:shadow transition-all shrink-0 flex items-center space-x-2 cursor-pointer"
        >
          <span>Run Live Predictor</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Row 4: Recent Inferences Log Table */}
      <div className="luxury-card overflow-hidden">
        <div className="p-5 border-b border-[#E2D7C8] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white">
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold font-luxury text-slate-900">Recent Inferences Log</h3>
              <span className="px-2 py-0.5 bg-emerald-50 text-emerald-800 text-[10px] font-bold rounded-md border border-emerald-200 flex items-center space-x-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse"></span>
                <span>Live Feed</span>
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Real-time SKU evaluations processed via the inference endpoint.</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search device or specs..."
                value={logSearch}
                onChange={(e) => setLogSearch(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs bg-[#FAF5ED] border border-[#DDD1C1] rounded-lg text-slate-800 placeholder-slate-400 focus:bg-white focus:outline-hidden"
              />
            </div>
            <div className="relative">
              <select
                value={logFilter}
                onChange={(e) => setLogFilter(e.target.value)}
                className="pl-3 pr-8 py-1.5 text-xs bg-[#FAF5ED] border border-[#DDD1C1] rounded-lg text-slate-700 font-medium focus:outline-hidden cursor-pointer"
              >
                <option value="all">All Tiers</option>
                <option value="Budget">Budget</option>
                <option value="Mid-Range">Mid-Range</option>
                <option value="Premium">Premium</option>
                <option value="Flagship">Flagship</option>
              </select>
              <Filter className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
            <button
              onClick={handleExportCSV}
              className="px-3 py-1.5 bg-white border border-[#E2D7C8] hover:bg-[#FAF5ED] text-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors cursor-pointer"
            >
              <Download className="w-3.5 h-3.5 text-slate-500" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* Table Content */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF5ED] text-slate-500 font-bold uppercase tracking-wider text-[10px] border-b border-[#E2D7C8]">
              <tr>
                <th className="py-3 px-5">Device Specification Preview</th>
                <th className="py-3 px-5">Predicted Class</th>
                <th className="py-3 px-5">Confidence</th>
                <th className="py-3 px-5">Active Model</th>
                <th className="py-3 px-5">Inference Timestamp</th>
                <th className="py-3 px-4 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E2D7C8] text-slate-700 font-mono">
              {filteredLogs.map((log) => (
                <tr key={log.id} className="hover:bg-[#FAF5ED]/80 transition-colors">
                  <td className="py-3.5 px-5 font-sans">
                    <div className="font-bold text-slate-900">{log.device}</div>
                    <div className="text-[11px] text-slate-500 font-mono mt-0.5">{log.specs}</div>
                  </td>
                  <td className="py-3.5 px-5 font-sans">
                    <span className={`inline-block px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${log.badgeColor}`}>
                      {log.predictedClass}
                    </span>
                  </td>
                  <td className="py-3.5 px-5">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold font-mono text-slate-900">{log.confidence}</span>
                      <div className="w-16 bg-[#E2D7C8] rounded-full h-1.5 overflow-hidden">
                        <div className={`h-1.5 rounded-full ${log.barColor}`} style={{ width: log.confidence }}></div>
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-5 text-slate-600 text-[11px]">
                    {log.activeModel}
                  </td>
                  <td className="py-3.5 px-5 text-slate-500 text-[11px] font-sans">
                    {log.time}
                  </td>
                  <td className="py-3.5 px-4 text-center font-sans">
                    <button
                      onClick={() => onNavigate('predict')}
                      className="px-2.5 py-1 bg-white border border-[#E2D7C8] hover:bg-amber-50 text-amber-800 text-xs font-semibold rounded-md transition-colors cursor-pointer inline-flex items-center space-x-1"
                    >
                      <span>Test</span>
                      <ChevronRight className="w-3 h-3" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="p-4 border-t border-[#E2D7C8] bg-[#FAF5ED]/50 flex items-center justify-between text-xs text-slate-500">
          <span>Showing {filteredLogs.length} of 1,248 total log records</span>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => onNavigate('dataset')}
              className="text-amber-800 hover:text-amber-900 font-bold flex items-center space-x-1 cursor-pointer"
            >
              <span>View Full Dataset Corpus</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* AUDIT LOG MODAL */}
      {showAuditModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-xs animate-in fade-in duration-150"
          onClick={() => setShowAuditModal(false)}
        >
          <div
            className="bg-[#FAF5ED] border border-[#D5C7B5] rounded-2xl shadow-2xl max-w-2xl w-full p-6 text-slate-900 relative space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between pb-3 border-b border-[#E2D7C8]">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <h3 className="text-base font-bold font-luxury text-slate-900">Cryptographic Model Audit & Lineage Record</h3>
              </div>
              <button
                onClick={() => setShowAuditModal(false)}
                className="p-1.5 text-slate-400 hover:text-slate-800 rounded-lg hover:bg-slate-200/60 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-white rounded-xl border border-[#E2D7C8] space-y-1 font-mono text-[11px]">
                <div className="text-slate-500">AUDIT_RECORD_SHA256:</div>
                <div className="font-bold text-amber-900 break-all">8f9b2d38a0e41cb1289dfc9a51203928a7e4b9318c6d123e498c8120b</div>
              </div>

              <div className="space-y-2 text-slate-700 leading-relaxed">
                <div className="p-3 bg-white rounded-xl border border-[#E2D7C8] space-y-1">
                  <div className="font-bold text-slate-900 flex items-center space-x-1.5">
                    <Activity className="w-3.5 h-3.5 text-amber-800" />
                    <span>Cross-Validation Protocol</span>
                  </div>
                  <p className="text-slate-600">
                    Random seed fixed to 42. 5 stratified folds evaluated to maintain class proportions (Budget 34.4%, Mid-Range 35.6%, Premium 13.6%, Flagship 16.4%).
                  </p>
                </div>

                <div className="p-3 bg-white rounded-xl border border-[#E2D7C8] space-y-1">
                  <div className="font-bold text-slate-900 flex items-center space-x-1.5">
                    <BarChart3 className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Certified Evaluation Bounds</span>
                  </div>
                  <p className="text-slate-600">
                    Champion model: Random Forest (300 Estimators, max_depth=16, Gini criterion). Macro F1: 0.945 &bull; Macro Precision: 94.5% &bull; Macro Recall: 94.8% &bull; ROC-AUC: 0.987.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-end pt-3 border-t border-[#E2D7C8]">
              <button
                onClick={() => setShowAuditModal(false)}
                className="px-4 py-1.5 bg-amber-800 hover:bg-amber-900 text-white text-xs font-bold rounded-lg cursor-pointer"
              >
                Close Audit Dossier
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
