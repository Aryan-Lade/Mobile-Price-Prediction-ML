import {
  LayoutGrid,
  Smartphone,
  FlaskConical,
  Database,
  Sparkles,
  PanelLeftClose,
  X
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  apiOnline: boolean | null;
  mobileMenuOpen?: boolean;
  onCloseMobileMenu?: () => void;
  sidebarHidden?: boolean;
  onToggleSidebar?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  apiOnline,
  mobileMenuOpen = false,
  onCloseMobileMenu,
  sidebarHidden = false,
  onToggleSidebar
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutGrid },
    { id: 'predict', label: 'Predict', icon: Smartphone },
    { id: 'model-lab', label: 'Model Lab', icon: FlaskConical },
    { id: 'dataset', label: 'Dataset', icon: Database },
  ];

  const handleNavClick = (tabId: string) => {
    setActiveTab(tabId);
    if (onCloseMobileMenu) {
      onCloseMobileMenu();
    }
  };

  const NavContent = (
    <div className="flex flex-col justify-between h-full">
      <div>
        {/* Logo & Brand Header */}
        <div className="p-4 sm:p-5 border-b border-[#E2D7C8] flex items-center justify-between bg-white/70">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-900 via-amber-950 to-slate-900 flex items-center justify-center text-amber-200 shadow-sm font-bold text-lg border border-amber-600/30 shrink-0">
              <Sparkles className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <div className="font-luxury font-bold text-slate-900 text-lg leading-tight tracking-tight">SmartPrice</div>
              <div className="text-[10px] font-semibold tracking-widest text-amber-800/80 uppercase">Price Intelligence</div>
            </div>
          </div>
          <div className="flex items-center space-x-1">
            {/* Desktop Hide Sidebar Trigger */}
            {onToggleSidebar && (
              <button
                onClick={onToggleSidebar}
                className="hidden lg:flex p-1.5 rounded-lg text-slate-400 hover:text-amber-950 hover:bg-[#EFE7DC] active:scale-95 transition-all cursor-pointer"
                title="Hide Sidebar (Ctrl+B)"
                aria-label="Hide Sidebar"
              >
                <PanelLeftClose className="w-4.5 h-4.5" />
              </button>
            )}
            {/* Mobile Close Button */}
            {onCloseMobileMenu && (
              <button
                onClick={onCloseMobileMenu}
                className="lg:hidden p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 cursor-pointer"
                aria-label="Close Mobile Navigation"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>

        {/* Platform Navigation */}
        <div className="p-4">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 mb-2">
            Platform
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`w-full flex items-center space-x-3 px-3.5 py-3 lg:py-2.5 rounded-lg text-sm font-medium transition-all text-left cursor-pointer ${
                    isActive
                      ? 'bg-white text-amber-900 font-semibold shadow-xs border border-[#D8CABE]'
                      : 'text-slate-600 hover:text-slate-950 hover:bg-white/70'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-amber-800' : 'text-slate-400'}`} />
                  <span className={isActive ? 'font-semibold' : ''}>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Bottom System Status */}
      <div className="p-4 border-t border-[#E2D7C8] bg-white/80">
        <div className="flex items-center justify-between text-xs mb-1.5">
          <div className="flex items-center space-x-2">
            <span className={`w-2 h-2 rounded-full ${apiOnline ? 'bg-emerald-500 animate-pulse' : apiOnline === false ? 'bg-rose-500' : 'bg-amber-400'}`} />
            <span className="font-medium text-slate-700">ML system online</span>
          </div>
          <span className="text-emerald-700 font-semibold text-xs">{apiOnline ? '100%' : 'Offline'}</span>
        </div>
        <div className="text-[10px] font-mono text-slate-400 flex justify-between">
          <span>BUILD VERSION</span>
          <span className="text-amber-900/70 font-semibold">v1.2.4</span>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Collapsible/Hideable Sidebar */}
      <aside
        className={`hidden lg:flex flex-col justify-between shrink-0 min-h-screen sticky top-0 h-screen z-30 transition-all duration-300 ease-in-out bg-[#FAF5ED] border-r border-[#E2D7C8] shadow-[1px_0_12px_rgba(50,35,20,0.03)] overflow-hidden ${
          sidebarHidden ? 'w-0 min-w-0 border-r-0 opacity-0 pointer-events-none' : 'w-64 min-w-[16rem] opacity-100'
        }`}
      >
        <div className="w-64 h-full flex flex-col justify-between">
          {NavContent}
        </div>
      </aside>

      {/* Mobile Slide-Over Drawer with Backdrop */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Backdrop overlay */}
          <div
            onClick={onCloseMobileMenu}
            className="fixed inset-0 bg-slate-950/40 backdrop-blur-xs transition-opacity duration-300 animate-in fade-in"
          />

          {/* Drawer container */}
          <div className="fixed inset-y-0 left-0 max-w-[280px] w-full bg-[#FAF5ED] border-r border-[#E2D7C8] shadow-2xl z-50 flex flex-col justify-between animate-in slide-in-from-left duration-250">
            {NavContent}
          </div>
        </div>
      )}
    </>
  );
};
