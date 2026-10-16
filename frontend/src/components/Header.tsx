import React from 'react';
import { Search, CheckCircle2, Activity, Menu, PanelLeft } from 'lucide-react';

interface HeaderProps {
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
  onOpenMobileMenu?: () => void;
  sidebarHidden?: boolean;
  onToggleSidebar?: () => void;
  activeTab?: string;
}

export const Header: React.FC<HeaderProps> = ({
  searchQuery = '',
  setSearchQuery,
  onOpenMobileMenu,
  sidebarHidden = false,
  onToggleSidebar,
  activeTab = 'dashboard'
}) => {
  const tabTitles: Record<string, string> = {
    'dashboard': 'Executive Overview',
    'predict': 'Live Inference Engine',
    'model-lab': 'Benchmarking & Metrics',
    'dataset': 'Verified Registry'
  };

  return (
    <header className="h-16 bg-[#FAF5ED]/95 backdrop-blur-md border-b border-[#E2D7C8] px-4 sm:px-6 flex items-center justify-between sticky top-0 z-20 shadow-[0_1px_6px_rgba(50,35,20,0.02)] transition-all">
      {/* Left controls: Sidebar toggle & Search */}
      <div className="flex items-center space-x-2 sm:space-x-3 flex-1 max-w-2xl">
        {/* Mobile Hamburger Button */}
        <button
          onClick={onOpenMobileMenu}
          className="lg:hidden p-2 rounded-lg bg-white border border-[#DDD1C1] text-amber-900 hover:bg-[#FAF5ED] active:scale-95 transition-all cursor-pointer shrink-0 shadow-2xs"
          aria-label="Open Mobile Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Desktop Sidebar Hide/Show Toggle Button */}
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            className={`hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-lg border transition-all cursor-pointer shrink-0 shadow-2xs text-xs font-semibold ${
              sidebarHidden
                ? 'bg-amber-100/70 border-amber-400/80 text-amber-950 hover:bg-amber-100'
                : 'bg-white border-[#DDD1C1] text-slate-700 hover:text-amber-950 hover:bg-[#FAF5ED] hover:border-amber-400/50'
            }`}
            title={sidebarHidden ? "Show Sidebar (Ctrl+B)" : "Hide Sidebar (Ctrl+B)"}
            aria-label={sidebarHidden ? "Show Sidebar" : "Hide Sidebar"}
          >
            <PanelLeft className={`w-4 h-4 transition-transform duration-200 ${sidebarHidden ? 'text-amber-800 scale-105' : 'text-slate-500'}`} />
            <span className="text-[11px] font-semibold">
              {sidebarHidden ? "Show Sidebar" : "Hide Sidebar"}
            </span>
            <kbd className="hidden xl:inline-block px-1.5 py-0.5 bg-[#F4EEE6] text-[10px] text-slate-500 font-mono rounded-xs border border-[#DDD1C1]">
              Ctrl+B
            </kbd>
          </button>
        )}

        {/* Search Spec Input */}
        <div className="relative flex-1 min-w-[140px] max-w-md">
          <Search className="w-4 h-4 text-amber-900/40 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search spec, SoC, brand..."
            value={searchQuery}
            onChange={(e) => setSearchQuery && setSearchQuery(e.target.value)}
            className="w-full pl-9.5 pr-8 py-2 bg-white hover:bg-white focus:bg-white text-xs text-slate-800 placeholder-slate-400 rounded-lg border border-[#DDD1C1] focus:outline-hidden focus:ring-2 focus:ring-amber-700/15 focus:border-amber-800/50 transition-all shadow-2xs"
          />
          <kbd className="hidden sm:inline-block absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] text-slate-400 font-mono px-1 py-0.5 bg-slate-50 border border-slate-200 rounded">
            /
          </kbd>
        </div>

        {/* Verified Phones Pill */}
        <div className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 bg-white border border-[#DDD1C1] rounded-lg text-xs text-amber-900 font-medium shrink-0 shadow-2xs">
          <CheckCircle2 className="w-3.5 h-3.5 text-amber-700" />
          <span><strong className="font-semibold text-slate-900">980</strong> phones verified</span>
        </div>
      </div>

      {/* Right controls: Active Workspace Badge & Lab Status */}
      <div className="flex items-center space-x-2 sm:space-x-3 ml-2 sm:ml-4">
        {/* Active View Indicator */}
        <div className="hidden lg:flex items-center px-2.5 py-1 bg-[#F4EEE6] border border-[#E2D7C8] rounded-md text-[11px] font-medium text-slate-600">
          <span className="text-slate-400 mr-1.5">View:</span>
          <span className="font-semibold text-slate-800">{tabTitles[activeTab] || 'Workspace'}</span>
        </div>

        {/* Lab Project Details Badge */}
        <div className="flex items-center space-x-2 px-2.5 sm:px-3 py-1.5 bg-white border border-[#DDD1C1] rounded-lg text-xs shadow-2xs">
          <Activity className="w-3.5 h-3.5 text-emerald-600" />
          <span className="font-semibold text-slate-800 text-[11px] sm:text-xs">SmartPrice Lab</span>
          <span className="hidden md:inline text-slate-300">•</span>
          <span className="hidden md:inline text-slate-500 text-[11px]">Academic</span>
        </div>
      </div>
    </header>
  );
};
