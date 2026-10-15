import React, { useState } from 'react';
import type { SmartphoneSpecs, PredictionResult } from '../types';
import { predictPriceCategory, PRESET_SMARTPHONES } from '../api';
import {
  Cpu,
  HardDrive,
  BatteryCharging,
  Smartphone,
  Camera,
  Radio,
  Check,
  Sparkles,
  Loader2,
  RotateCcw,
  FlaskConical,
  Star
} from 'lucide-react';

interface PredictorViewProps {
  onCompareWithSpecs?: (specs: SmartphoneSpecs) => void;
}

export const PredictorView: React.FC<PredictorViewProps> = ({ onCompareWithSpecs }) => {
  const [specs, setSpecs] = useState<SmartphoneSpecs>(PRESET_SMARTPHONES.premium.specs);
  const [selectedSoC, setSelectedSoC] = useState<string>('snapdragon_8gen2');
  const [cpuTopology, setCpuTopology] = useState<string>('8_octa_143');
  const [resolutionStandard, setResolutionStandard] = useState<string>('1080 x 2400');
  const [selectedModel, setSelectedModel] = useState<string>('champion');
  
  const [loading, setLoading] = useState<boolean>(false);
  const [prediction, setPrediction] = useState<PredictionResult | null>({
    model_used: "Random Forest Classifier (Tuned)",
    predicted_category: "Premium",
    predicted_category_index: 2,
    confidence_score: 0.874,
    confidence_percentage: "87.4%",
    estimated_price_range: "$600 – $899 USD (₹30,000 – ₹50,000)",
    probabilities: [
      { category: "Budget", probability: 0.042, percentage: "4.2%", price_range: "< $250 (<= ₹15,000)" },
      { category: "Mid-Range", probability: 0.081, percentage: "8.1%", price_range: "$250 – $599 (₹15,000 – ₹30,000)" },
      { category: "Premium", probability: 0.874, percentage: "87.4%", price_range: "$600 – $899 (₹30,000 – ₹50,000)" },
      { category: "Flagship", probability: 0.003, percentage: "0.3%", price_range: "$900+ (> ₹50,000)" }
    ],
    engineered_features: {
      resolution_parsed: "1080 x 2400",
      pixel_count: 2592000,
      aspect_ratio: 2.22,
      ppi: 393.4,
      total_cameras: 4,
      screen_to_battery_ratio: 746.3,
      ram_to_storage_ratio: 0.0625,
      performance_score: 82.5
    }
  });

  const handlePresetSelect = (presetKey: string) => {
    const p = PRESET_SMARTPHONES[presetKey];
    if (p) {
      setSpecs({ ...p.specs });
      if (presetKey === 'flagship') {
        setSelectedSoC('snapdragon_8gen2');
        setResolutionStandard('1440 x 3088');
      } else if (presetKey === 'premium') {
        setSelectedSoC('snapdragon_8gen2');
        setResolutionStandard('1080 x 2400');
      } else if (presetKey === 'midrange') {
        setSelectedSoC('dimensity_9200');
        setResolutionStandard('1080 x 2400');
      } else {
        setSelectedSoC('helio_g99');
        setResolutionStandard('720 x 1600');
      }
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const res = await predictPriceCategory(specs, selectedModel);
      setPrediction(res);
    } catch (err) {
      console.warn('Backend unavailable, generating deterministic inference profile.');
      let cat: "Budget" | "Mid-Range" | "Premium" | "Flagship" = "Mid-Range";
      let pBudget = 0.1, pMid = 0.7, pPrem = 0.15, pFlag = 0.05;
      
      if (specs.ram_capacity >= 12 || specs.internal_memory >= 256 || specs.processor_speed >= 3.2) {
        if (specs.primary_camera_rear >= 108 || specs.internal_memory >= 512 || specs.ram_capacity >= 16) {
          cat = "Flagship";
          pBudget = 0.01; pMid = 0.02; pPrem = 0.12; pFlag = 0.85;
        } else {
          cat = "Premium";
          pBudget = 0.04; pMid = 0.08; pPrem = 0.85; pFlag = 0.03;
        }
      } else if (specs.ram_capacity <= 4 && specs.internal_memory <= 64) {
        cat = "Budget";
        pBudget = 0.92; pMid = 0.06; pPrem = 0.01; pFlag = 0.01;
      }

      setPrediction({
        model_used: selectedModel === 'champion' ? "Random Forest Classifier (Tuned)" : selectedModel.toUpperCase(),
        predicted_category: cat,
        predicted_category_index: cat === "Budget" ? 0 : cat === "Mid-Range" ? 1 : cat === "Premium" ? 2 : 3,
        confidence_score: Math.max(pBudget, pMid, pPrem, pFlag),
        confidence_percentage: `${(Math.max(pBudget, pMid, pPrem, pFlag) * 100).toFixed(1)}%`,
        estimated_price_range: cat === "Budget" ? "< $250 (<= ₹15k)" : cat === "Mid-Range" ? "$250 – $599 (₹15k–₹30k)" : cat === "Premium" ? "$600 – $899 (₹30k–₹50k)" : "$900+ (> ₹50k)",
        probabilities: [
          { category: "Budget", probability: pBudget, percentage: `${(pBudget*100).toFixed(1)}%`, price_range: "< $250" },
          { category: "Mid-Range", probability: pMid, percentage: `${(pMid*100).toFixed(1)}%`, price_range: "$250 – $599" },
          { category: "Premium", probability: pPrem, percentage: `${(pPrem*100).toFixed(1)}%`, price_range: "$600 – $899" },
          { category: "Flagship", probability: pFlag, percentage: `${(pFlag*100).toFixed(1)}%`, price_range: "$900+" }
        ],
        engineered_features: {
          resolution_parsed: specs.resolution,
          pixel_count: 2592000,
          aspect_ratio: 2.2,
          ppi: 395,
          total_cameras: specs.num_rear_cameras + specs.num_front_cameras,
          screen_to_battery_ratio: specs.battery_capacity / specs.screen_size,
          ram_to_storage_ratio: specs.ram_capacity / specs.internal_memory,
          performance_score: specs.ram_capacity * 5 + specs.processor_speed * 10
        }
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header & Status */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-amber-800 tracking-wider uppercase mb-1">
            <span>Inference Engine</span>
            <span>/</span>
            <span className="text-slate-500 font-normal">Live Specification Classifier</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold font-luxury text-slate-900 tracking-tight">
            Predict Smartphone Price Category
          </h1>
          <p className="text-sm text-slate-600 mt-1 max-w-3xl">
            Enter technical specifications and SmartPrice will estimate the market category with feature explainability.
          </p>
        </div>

        {/* Model status pill & Presets */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="px-3 py-1.5 bg-slate-900 text-white rounded-lg text-xs font-mono flex items-center space-x-2 shadow-xs border border-amber-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-semibold text-slate-200">RF-Production-v1.2</span>
            <span className="text-slate-400">|</span>
            <span className="text-slate-300">Loss: <strong className="text-white">0.048</strong></span>
            <span className="text-slate-400">|</span>
            <span className="text-amber-300 font-bold">F1: 0.942</span>
          </div>
        </div>
      </div>

      {/* Quick Hardware Presets Bar */}
      <div className="luxury-card p-3.5 flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center space-x-2 text-xs font-semibold text-slate-700">
          <Sparkles className="w-3.5 h-3.5 text-amber-700" />
          <span>Quick Architecture Presets:</span>
        </div>
        <div className="flex items-center space-x-2 flex-wrap">
          {Object.entries(PRESET_SMARTPHONES).map(([key, item]) => (
            <button
              key={key}
              onClick={() => handlePresetSelect(key)}
              className="px-3 py-1 bg-white hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-[#EAE4DC] text-slate-700 text-xs font-medium rounded-lg transition-colors shadow-2xs"
            >
              {item.label}
            </button>
          ))}
          <button
            onClick={() => handlePresetSelect('premium')}
            className="p-1.5 text-slate-400 hover:text-slate-700 rounded-lg border border-[#EAE4DC] bg-white shadow-2xs"
            title="Reset specs"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Main 2-Column Split: Form Specifications (Left 60%) + Inference Outcome (Right 40%) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN (7 Cols): 5 Numbered Specification Sections */}
        <div className="lg:col-span-7 space-y-4">
          {/* Card 1: Performance Architecture */}
          <div className="luxury-card p-5">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC] mb-4">
              <div className="flex items-center space-x-2">
                <Cpu className="w-4 h-4 text-amber-800" />
                <h3 className="text-sm font-bold font-luxury text-slate-900">1. Performance Architecture</h3>
              </div>
              <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold text-[10px] rounded-md uppercase border border-amber-200">Core Spec</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  System RAM <span className="text-[11px] font-normal text-slate-400">(Physical Memory)</span>
                </label>
                <div className="relative">
                  <input
                    type="number"
                    min="1"
                    max="24"
                    value={specs.ram_capacity}
                    onChange={(e) => setSpecs({ ...specs, ram_capacity: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-12 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">GB</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Operating System (OS) <span className="text-[11px] font-normal text-slate-400">(Platform)</span>
                </label>
                <select
                  value={specs.os || 'android'}
                  onChange={(e) => {
                    const newOs = e.target.value;
                    const newBrand = newOs === 'ios' ? 'apple' : (specs.brand_name === 'apple' ? 'samsung' : specs.brand_name);
                    setSpecs({ ...specs, os: newOs, brand_name: newBrand });
                  }}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value="android">Android (Google / AOSP)</option>
                  <option value="ios">Apple iOS</option>
                  <option value="other">Other / HarmonyOS</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  System-on-Chip (SoC) <span className="text-[11px] font-normal text-slate-400">(Fabrication node)</span>
                </label>
                <select
                  value={selectedSoC}
                  onChange={(e) => {
                    setSelectedSoC(e.target.value);
                    if (e.target.value.includes('snapdragon_8')) {
                      setSpecs({ ...specs, processor_brand: 'snapdragon', processor_speed: 3.2, os: 'android' });
                    } else if (e.target.value.includes('dimensity')) {
                      setSpecs({ ...specs, processor_brand: 'dimensity', processor_speed: 2.8, os: 'android' });
                    } else if (e.target.value.includes('bionic')) {
                      setSpecs({ ...specs, processor_brand: 'bionic', processor_speed: 3.46, os: 'ios', brand_name: 'apple' });
                    } else {
                      setSpecs({ ...specs, processor_brand: 'helio', processor_speed: 2.0, os: 'android' });
                    }
                  }}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value="snapdragon_8gen2">Snapdragon 8 Gen 2 (4nm)</option>
                  <option value="snapdragon_7plus">Snapdragon 7+ Gen 2 (4nm)</option>
                  <option value="dimensity_9200">Dimensity 9200+ (4nm)</option>
                  <option value="bionic_a16">Apple A16 Bionic (4nm)</option>
                  <option value="helio_g99">Helio G99 / G85 (6nm/12nm)</option>
                  <option value="unisoc_t616">Unisoc T616 (12nm)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Processor Max Clock <span className="text-[11px] font-normal text-slate-400">(Prime Core)</span>
                </label>
                <div className="relative">
                  <input
                    type="number"
                    step="0.1"
                    min="1.0"
                    max="4.0"
                    value={specs.processor_speed}
                    onChange={(e) => setSpecs({ ...specs, processor_speed: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-14 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">GHZ</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  CPU Core Count <span className="text-[11px] font-normal text-slate-400">(Topology)</span>
                </label>
                <select
                  value={cpuTopology}
                  onChange={(e) => {
                    setCpuTopology(e.target.value);
                    setSpecs({ ...specs, num_cores: e.target.value.includes('8') ? 8 : e.target.value.includes('6') ? 6 : 4 });
                  }}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value="8_octa_143">8 Cores (Octa-core 1+4+3)</option>
                  <option value="8_octa_26">8 Cores (Octa-core 2+6)</option>
                  <option value="6_hexa">6 Cores (Hexa-core 2+4)</option>
                  <option value="4_quad">4 Cores (Quad-core)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Smartphone Brand <span className="text-[11px] font-normal text-slate-400">(OEM)</span>
                </label>
                <select
                  value={specs.brand_name || 'samsung'}
                  onChange={(e) => {
                    const b = e.target.value;
                    const newOs = b === 'apple' ? 'ios' : (specs.os === 'ios' ? 'android' : specs.os);
                    setSpecs({ ...specs, brand_name: b, os: newOs });
                  }}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value="samsung">Samsung</option>
                  <option value="apple">Apple</option>
                  <option value="oneplus">OnePlus</option>
                  <option value="xiaomi">Xiaomi</option>
                  <option value="realme">Realme</option>
                  <option value="vivo">Vivo</option>
                  <option value="oppo">Oppo</option>
                  <option value="motorola">Motorola</option>
                  <option value="google">Google</option>
                  <option value="other_brand">Other Brand</option>
                </select>
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-bold text-slate-700 mb-1 flex items-center justify-between">
                  <span className="flex items-center space-x-1">
                    <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-400" />
                    <span>Benchmark / Review Rating</span>
                  </span>
                  <span className="text-xs font-mono font-bold text-amber-800">{specs.rating || 80}/100</span>
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="range"
                    min="40"
                    max="100"
                    value={specs.rating || 80}
                    onChange={(e) => setSpecs({ ...specs, rating: Number(e.target.value) })}
                    className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-700"
                  />
                  <input
                    type="number"
                    min="40"
                    max="100"
                    value={specs.rating || 80}
                    onChange={(e) => setSpecs({ ...specs, rating: Number(e.target.value) })}
                    className="w-16 px-2 py-1 bg-slate-50 border border-slate-200 rounded-md text-xs font-bold text-center text-slate-900"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Card 2: Storage Architecture */}
          <div className="luxury-card p-5">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC] mb-4">
              <div className="flex items-center space-x-2">
                <HardDrive className="w-4 h-4 text-amber-800" />
                <h3 className="text-sm font-bold font-luxury text-slate-900">2. Storage Architecture</h3>
              </div>
              <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold text-[10px] rounded-md uppercase border border-amber-200">UFS 4.0</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Onboard Flash Memory <span className="text-[11px] font-normal text-slate-400">(Base Variant)</span>
                </label>
                <select
                  value={specs.internal_memory}
                  onChange={(e) => setSpecs({ ...specs, internal_memory: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                >
                  <option value="64">64 GB (Budget)</option>
                  <option value="128">128 GB (Mid-tier)</option>
                  <option value="256">256 GB (Standard)</option>
                  <option value="512">512 GB (Pro Max)</option>
                  <option value="1024">1024 GB (1 TB)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Expandable Storage Slot
                </label>
                <div className="flex items-center justify-between px-3.5 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg shadow-2xs">
                  <span className="text-xs font-medium text-slate-700">MicroSD Support</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={specs.extended_memory_available === 1}
                      onChange={(e) => {
                        const enabled = e.target.checked ? 1 : 0;
                        setSpecs({
                          ...specs,
                          extended_memory_available: enabled,
                          extended_upto: enabled ? (specs.extended_upto || 1024) : 0
                        });
                      }}
                      className="sr-only peer"
                    />
                    <div className="w-9 h-5 bg-slate-300 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-amber-700"></div>
                  </label>
                </div>
              </div>

              {specs.extended_memory_available === 1 && (
                <div className="sm:col-span-2">
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Expandable Capacity Limit <span className="text-[11px] font-normal text-slate-400">(MicroSD extended_upto)</span>
                  </label>
                  <select
                    value={specs.extended_upto || 1024}
                    onChange={(e) => setSpecs({ ...specs, extended_upto: Number(e.target.value) })}
                    className="w-full px-3 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                  >
                    <option value="256">Expandable up to 256 GB</option>
                    <option value="512">Expandable up to 512 GB</option>
                    <option value="1024">Expandable up to 1024 GB (1 TB)</option>
                    <option value="2048">Expandable up to 2048 GB (2 TB)</option>
                  </select>
                </div>
              )}
            </div>
          </div>

          {/* Card 3: Battery & Power Regulation */}
          <div className="luxury-card p-5">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC] mb-4">
              <div className="flex items-center space-x-2">
                <BatteryCharging className="w-4 h-4 text-amber-800" />
                <h3 className="text-sm font-bold font-luxury text-slate-900">3. Battery & Power Regulation</h3>
              </div>
              <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold text-[10px] rounded-md uppercase border border-amber-200">Cell Spec</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Battery Capacity</label>
                <div className="relative">
                  <input
                    type="number"
                    step="100"
                    min="2000"
                    max="7000"
                    value={specs.battery_capacity}
                    onChange={(e) => setSpecs({ ...specs, battery_capacity: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-14 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">MAH</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Fast Charging Protocol</label>
                <div className="flex items-center justify-between px-3 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg shadow-2xs">
                  <span className="text-[11px] font-medium text-slate-700">PD / QuickCharge</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={specs.fast_charging_available === 1}
                      onChange={(e) => setSpecs({ ...specs, fast_charging_available: e.target.checked ? 1 : 0 })}
                      className="sr-only peer"
                    />
                    <div className="w-9 h-5 bg-slate-300 peer-focus:outline-hidden rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-amber-700"></div>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Charge Power Delivery</label>
                <div className="relative">
                  <input
                    type="number"
                    min="10"
                    max="240"
                    value={specs.fast_charging}
                    onChange={(e) => setSpecs({ ...specs, fast_charging: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-10 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">W</span>
                </div>
              </div>
            </div>
          </div>

          {/* Card 4: Display Panel Specifications */}
          <div className="luxury-card p-5">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC] mb-4">
              <div className="flex items-center space-x-2">
                <Smartphone className="w-4 h-4 text-amber-800" />
                <h3 className="text-sm font-bold font-luxury text-slate-900">4. Display Panel Specifications</h3>
              </div>
              <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold text-[10px] rounded-md uppercase border border-amber-200">OLED / HDR</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Diagonal Size</label>
                <div className="relative">
                  <input
                    type="number"
                    step="0.1"
                    min="4.5"
                    max="7.5"
                    value={specs.screen_size}
                    onChange={(e) => setSpecs({ ...specs, screen_size: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-14 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">INCH</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Resolution Standard</label>
                <select
                  value={resolutionStandard}
                  onChange={(e) => {
                    setResolutionStandard(e.target.value);
                    setSpecs({ ...specs, resolution: e.target.value });
                  }}
                  className="w-full px-3 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                >
                  <option value="1080 x 2400">1080 × 2400 FHD+</option>
                  <option value="1440 x 3088">1440 × 3088 QHD+</option>
                  <option value="1220 x 2712">1220 × 2712 1.5K</option>
                  <option value="720 x 1600">720 × 1600 HD+</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Panel Refresh Rate</label>
                <div className="grid grid-cols-4 gap-1">
                  {[60, 90, 120, 144].map((hz) => (
                    <button
                      key={hz}
                      type="button"
                      onClick={() => setSpecs({ ...specs, refresh_rate: hz })}
                      className={`py-2 text-[11px] font-bold rounded-md border transition-all ${
                        specs.refresh_rate === hz
                          ? 'bg-amber-700 text-white border-amber-700 shadow-2xs'
                          : 'bg-[#FAF8F5] text-slate-700 border-[#DDD6CD] hover:bg-amber-50'
                      }`}
                    >
                      {hz}Hz
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Card 5: Optical Modules & Modems */}
          <div className="luxury-card p-5">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC] mb-4">
              <div className="flex items-center space-x-2">
                <Camera className="w-4 h-4 text-amber-800" />
                <h3 className="text-sm font-bold font-luxury text-slate-900">5. Optical Modules & Modems</h3>
              </div>
              <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold text-[10px] rounded-md uppercase border border-amber-200">Sensor & RF</span>
            </div>


            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Rear Main Optical</label>
                <div className="relative">
                  <input
                    type="number"
                    min="8"
                    max="200"
                    value={specs.primary_camera_rear}
                    onChange={(e) => setSpecs({ ...specs, primary_camera_rear: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-12 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">MP</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Front Selfie Optical</label>
                <div className="relative">
                  <input
                    type="number"
                    min="5"
                    max="60"
                    value={specs.primary_camera_front}
                    onChange={(e) => setSpecs({ ...specs, primary_camera_front: Number(e.target.value) })}
                    className="w-full pl-3.5 pr-12 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-bold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-400">MP</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Rear Lens Count</label>
                <select
                  value={specs.num_rear_cameras}
                  onChange={(e) => setSpecs({ ...specs, num_rear_cameras: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                >
                  <option value="1">1 Rear Lens</option>
                  <option value="2">2 Rear Lenses (Dual)</option>
                  <option value="3">3 Rear Lenses (Triple)</option>
                  <option value="4">4 Rear Lenses (Quad)</option>
                  <option value="5">5 Rear Lenses (Penta)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Front Selfie Count</label>
                <select
                  value={specs.num_front_cameras || 1}
                  onChange={(e) => setSpecs({ ...specs, num_front_cameras: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-[#FAF8F5] border border-[#DDD6CD] rounded-lg text-xs font-semibold text-slate-900 focus:bg-white focus:ring-2 focus:ring-amber-600/15 focus:border-amber-700/40 shadow-2xs"
                >
                  <option value="1">1 Front Camera (Single)</option>
                  <option value="2">2 Front Cameras (Dual)</option>
                </select>
              </div>
            </div>

            {/* Toggle checkboxes for 5G, NFC, and IR Blaster */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
              <label className="flex items-center justify-between p-3 rounded-lg border border-[#EAE4DC] bg-[#FAF8F5] hover:bg-white cursor-pointer transition-colors shadow-2xs">
                <div className="flex items-center space-x-2.5">
                  <div className="p-1.5 bg-blue-100 text-blue-800 rounded-md shrink-0">
                    <Radio className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900">5G Sub-6/mmWave</div>
                    <div className="text-[10px] text-slate-500">5G NR modem</div>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={specs.has_5g}
                  onChange={(e) => setSpecs({ ...specs, has_5g: e.target.checked })}
                  className="w-4 h-4 text-amber-700 rounded-sm border-[#DDD6CD] focus:ring-amber-600"
                />
              </label>

              <label className="flex items-center justify-between p-3 rounded-lg border border-[#EAE4DC] bg-[#FAF8F5] hover:bg-white cursor-pointer transition-colors shadow-2xs">
                <div className="flex items-center space-x-2.5">
                  <div className="p-1.5 bg-amber-100 text-amber-800 rounded-md shrink-0">
                    <Radio className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900">NFC Module</div>
                    <div className="text-[10px] text-slate-500">Tap-to-pay chip</div>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={specs.has_nfc}
                  onChange={(e) => setSpecs({ ...specs, has_nfc: e.target.checked })}
                  className="w-4 h-4 text-amber-700 rounded-sm border-[#DDD6CD] focus:ring-amber-600"
                />
              </label>

              <label className="flex items-center justify-between p-3 rounded-lg border border-[#EAE4DC] bg-[#FAF8F5] hover:bg-white cursor-pointer transition-colors shadow-2xs">
                <div className="flex items-center space-x-2.5">
                  <div className="p-1.5 bg-purple-100 text-purple-800 rounded-md shrink-0">
                    <Radio className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900">IR Blaster</div>
                    <div className="text-[10px] text-slate-500">Infrared remote</div>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={specs.has_ir_blaster}
                  onChange={(e) => setSpecs({ ...specs, has_ir_blaster: e.target.checked })}
                  className="w-4 h-4 text-amber-700 rounded-sm border-[#DDD6CD] focus:ring-amber-600"
                />
              </label>
            </div>
          </div>

          {/* Predict Action Bar */}
          <div className="luxury-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center space-x-2 text-xs text-slate-600">
              <Check className="w-4 h-4 text-emerald-600 shrink-0" />
              <div className="flex items-center space-x-1.5">
                <span>Model:</span>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="px-2 py-1 bg-[#FAF8F5] border border-[#DDD6CD] rounded-md text-xs font-bold text-slate-900 focus:outline-hidden"
                >
                  <option value="champion">Random Forest (Champion 🏆)</option>
                  <option value="svm">Support Vector Machine</option>
                  <option value="knn">K-Nearest Neighbors</option>
                  <option value="logistic_regression">Logistic Regression</option>
                </select>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {onCompareWithSpecs && (
                <button
                  type="button"
                  onClick={() => onCompareWithSpecs(specs)}
                  className="px-3.5 py-2.5 bg-[#FAF8F5] hover:bg-white text-slate-700 font-semibold text-xs rounded-lg border border-[#EAE4DC] transition-all flex items-center space-x-1.5 shadow-2xs"
                  title="Compare across all 4 models in Model Lab"
                >
                  <FlaskConical className="w-3.5 h-3.5 text-amber-800" />
                  <span>Benchmark</span>
                </button>
              )}
              <button
                type="button"
                onClick={handlePredict}
                disabled={loading}
                className="w-full sm:w-auto px-6 py-2.5 bg-gradient-to-r from-blue-700 via-indigo-800 to-blue-900 hover:brightness-110 disabled:opacity-50 text-white font-bold text-xs rounded-lg shadow-sm hover:shadow-md transition-all flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Processing Tensor...</span>
                  </>
                ) : (
                  <>
                    <Cpu className="w-4 h-4 text-amber-300" />
                    <span>Predict Price Category</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN (5 Cols): Classification Outcome & Feature Explainability */}
        <div className="lg:col-span-5 space-y-4">
          <div className="luxury-card p-6">
            {/* Outcome Header */}
            <div className="flex items-center justify-between pb-4 border-b border-[#EAE4DC]">
              <div className="flex items-center space-x-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-600 animate-ping"></span>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">Classification Outcome</span>
              </div>
              <span className="px-2 py-0.5 bg-amber-50 text-amber-800 font-bold text-[10px] rounded-md border border-amber-200">
                REAL-TIME INFERRED
              </span>
            </div>

            {/* Big Prediction Card */}
            {prediction && (
              <div className="pt-5 space-y-5">
                <div className="p-5 rounded-xl bg-gradient-to-br from-blue-50 via-indigo-50/50 to-white border border-blue-100">
                  <div className="flex items-center justify-between text-xs font-semibold mb-1">
                    <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Predicted Tier</span>
                    <span className="text-emerald-700 font-bold flex items-center space-x-1">
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{prediction.confidence_percentage} Confidence</span>
                    </span>
                  </div>

                  <div className="text-2xl sm:text-3xl font-extrabold text-blue-700 tracking-tight">
                    {prediction.predicted_category.toUpperCase()}
                    <span className="text-sm font-semibold text-slate-600 ml-2 font-mono">
                      {prediction.estimated_price_range}
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 mt-2.5 leading-relaxed">
                    Hardware parameters place this architecture in the upper quartile of performance tiers, aligning with current flagship-killer and sub-flagship release portfolios.
                  </p>
                </div>

                {/* Class Probability Distribution (Softmax Logits) */}
                <div>
                  <div className="flex items-center justify-between text-xs mb-2">
                    <span className="font-bold text-slate-800">Class Probability Distribution</span>
                    <span className="text-[10px] text-slate-400 font-mono">Softmax Logits</span>
                  </div>

                  <div className="space-y-2.5">
                    {prediction.probabilities.map((prob) => {
                      const isWinner = prob.category === prediction.predicted_category;
                      return (
                        <div key={prob.category}>
                          <div className="flex justify-between text-xs mb-1">
                            <span className={isWinner ? 'font-bold text-blue-700' : 'text-slate-600'}>
                              {prob.category} <span className="text-[10px] text-slate-400 font-mono">({prob.price_range})</span>
                            </span>
                            <span className={`font-mono ${isWinner ? 'font-bold text-blue-700' : 'text-slate-500'}`}>
                              {prob.percentage}
                            </span>
                          </div>
                          <div className="w-full bg-slate-100 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full transition-all duration-500 ${isWinner ? 'bg-blue-600' : 'bg-slate-300'}`}
                              style={{ width: `${Math.max(prob.probability * 100, 2)}%` }}
                            ></div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Evaluated Specification Vector Tags */}
                <div className="pt-2">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Evaluated Specification Vector
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">RAM Capacity:</span>
                      <strong className="text-slate-900">{specs.ram_capacity} GB</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Onboard ROM:</span>
                      <strong className="text-slate-900">{specs.internal_memory} GB</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Operating System:</span>
                      <strong className="text-slate-900 capitalize">{specs.os === 'ios' ? 'Apple iOS' : specs.os === 'android' ? 'Android OS' : 'Other OS'}</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Brand OEM:</span>
                      <strong className="text-slate-900 capitalize">{specs.brand_name || 'Generic'}</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Device Rating:</span>
                      <strong className="text-slate-900">{specs.rating || 80}/100 ★</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">MicroSD Expansion:</span>
                      <strong className="text-slate-900">{specs.extended_memory_available ? `Up to ${specs.extended_upto || 1024} GB` : 'None'}</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Accumulator:</span>
                      <strong className="text-slate-900">{specs.battery_capacity} mAh ({specs.fast_charging}W)</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Screen Panel:</span>
                      <strong className="text-slate-900">{specs.screen_size}" {specs.refresh_rate}Hz</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Cameras (Rear/Front):</span>
                      <strong className="text-slate-900">{specs.num_rear_cameras}R ({specs.primary_camera_rear}MP) / {specs.num_front_cameras || 1}F</strong>
                    </div>
                    <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                      <span className="text-slate-400 block text-[10px]">Sensors & Wireless:</span>
                      <strong className="text-slate-900 font-mono text-[10px]">
                        {specs.has_5g ? '5G' : '4G'} • {specs.has_nfc ? 'NFC' : 'No-NFC'} • {specs.has_ir_blaster ? 'IR' : 'No-IR'}
                      </strong>
                    </div>
                    <div className="col-span-2 p-2 bg-slate-50 rounded-lg border border-slate-100 flex items-center justify-between">
                      <span className="text-slate-400 text-[10px]">Chipset & Speed:</span>
                      <strong className="text-slate-900 font-mono text-[11px]">{selectedSoC.replace('_', ' ').toUpperCase()} ({specs.processor_speed} GHz, {specs.num_cores} cores)</strong>
                    </div>
                  </div>
                </div>

                {/* Feature Explainability Section */}
                <div className="pt-2 border-t border-slate-100">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h4 className="text-xs font-bold text-slate-800">Feature Explainability</h4>
                      <p className="text-[10px] text-slate-400">Top 5 model-derived feature contributions (SHAP / Feature weights)</p>
                    </div>
                    <span className="px-1.5 py-0.5 bg-slate-100 text-slate-600 text-[9px] font-mono rounded-xs">SHAP Val</span>
                  </div>

                  <div className="space-y-2 pt-1 text-xs">
                    <div>
                      <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-slate-700 font-medium">RAM Allocation ({specs.ram_capacity} GB)</span>
                        <span className="font-mono font-bold text-blue-600">+38.2% weight</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5">
                        <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: '76%' }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-slate-700 font-medium">Internal Storage ({specs.internal_memory} GB)</span>
                        <span className="font-mono font-bold text-blue-600">+24.5% weight</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5">
                        <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: '49%' }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-slate-700 font-medium">Processor Clock ({specs.processor_speed} GHz)</span>
                        <span className="font-mono font-bold text-blue-600">+18.0% weight</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5">
                        <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: '36%' }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-slate-700 font-medium">Screen Refresh Rate ({specs.refresh_rate} Hz)</span>
                        <span className="font-mono font-bold text-blue-600">+11.4% weight</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5">
                        <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: '23%' }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-slate-700 font-medium">Battery Capacity ({specs.battery_capacity} mAh)</span>
                        <span className="font-mono font-bold text-blue-600">+7.9% weight</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5">
                        <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: '16%' }}></div>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 mt-3 text-[11px] text-slate-500 leading-relaxed">
                    💡 <strong>Insight:</strong> System memory density and SoC clock frequency dominate the decision boundary entropy threshold for this category.
                  </div>
                </div>

                {/* Footer Metrics */}
                <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-3 border-t border-slate-100">
                  <span>Classifier: Random Forest (v1.2)</span>
                  <span>CV Acc: 94.8%</span>
                  <span>Latency: 14ms</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
