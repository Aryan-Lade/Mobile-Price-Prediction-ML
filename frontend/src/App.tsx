import { useState, useEffect } from 'react';
import type { SmartphoneSpecs } from './types';
import { PRESET_SMARTPHONES, checkApiHealth } from './api';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardView } from './components/DashboardView';
import { PredictorView } from './components/PredictorView';
import { ModelBenchmarkingView } from './components/ModelBenchmarkingView';
import { DatasetAnalyticsView } from './components/DatasetAnalyticsView';
import { BottomNav } from './components/BottomNav';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [activeSpecs, setActiveSpecs] = useState<SmartphoneSpecs>(PRESET_SMARTPHONES.flagship.specs);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);
  const [sidebarHidden, setSidebarHidden] = useState<boolean>(() => {
    try {
      return localStorage.getItem('smartprice_sidebar_hidden') === 'true';
    } catch {
      return false;
    }
  });

  const handleToggleSidebar = () => {
    setSidebarHidden((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('smartprice_sidebar_hidden', String(next));
      } catch {}
      return next;
    });
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault();
        handleToggleSidebar();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await checkApiHealth();
        setApiOnline(res.status === 'healthy');
      } catch (e) {
        setApiOnline(false);
      }
    }
    checkHealth();
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  const handleCompareWithSpecs = (specs: SmartphoneSpecs) => {
    setActiveSpecs(specs);
    setActiveTab('model-lab');
  };

  return (
    <div className="min-h-screen bg-[#F4EEE6] text-slate-900 flex font-sans antialiased selection:bg-amber-800 selection:text-white">
      {/* Sidebar: Collapsible/Hideable on Desktop, Slide-over on Mobile */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiOnline={apiOnline}
        mobileMenuOpen={mobileMenuOpen}
        onCloseMobileMenu={() => setMobileMenuOpen(false)}
        sidebarHidden={sidebarHidden}
        onToggleSidebar={handleToggleSidebar}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out">
        {/* Top Header with Mobile Hamburger & Desktop Sidebar Toggle Trigger */}
        <Header
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onOpenMobileMenu={() => setMobileMenuOpen(true)}
          sidebarHidden={sidebarHidden}
          onToggleSidebar={handleToggleSidebar}
          activeTab={activeTab}
        />

        {/* Dynamic Workspace Views with Glitch-Free Persistent Mounting */}
        <main className="flex-1 px-3 sm:px-6 py-4 sm:py-7 pb-24 lg:pb-8 max-w-7xl w-full mx-auto">
          <div className={activeTab === 'dashboard' ? 'tab-pane active' : 'tab-pane'}>
            <DashboardView onNavigate={(tab) => setActiveTab(tab)} />
          </div>

          <div className={activeTab === 'predict' ? 'tab-pane active' : 'tab-pane'}>
            <PredictorView onCompareWithSpecs={handleCompareWithSpecs} />
          </div>

          <div className={activeTab === 'model-lab' ? 'tab-pane active' : 'tab-pane'}>
            <ModelBenchmarkingView currentSpecs={activeSpecs} />
          </div>

          <div className={activeTab === 'dataset' ? 'tab-pane active' : 'tab-pane'}>
            <DatasetAnalyticsView />
          </div>
        </main>

        {/* Clean Luxury Footer */}
        <footer className="border-t border-[#E2D7C8] bg-[#FAF5ED] py-4 px-4 sm:px-6 mb-16 lg:mb-0 mt-auto">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-800 font-luxury">SmartPrice Intelligence Platform</span>
              <span>•</span>
              <span className="text-amber-900/70 font-medium">Academic Research Benchmark</span>
            </div>
            <div className="text-slate-400 font-mono text-[11px]">
              FastAPI Server (Port 8000) • Scikit-Learn 1.8.0 • React 19 + TypeScript
            </div>
          </div>
        </footer>

        {/* Mobile Persistent 1-Thumb Bottom Navigation */}
        <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
    </div>
  );
}

export default App;
