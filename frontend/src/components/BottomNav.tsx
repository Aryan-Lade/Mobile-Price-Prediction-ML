import React from 'react';
import {
  LayoutGrid,
  Smartphone,
  FlaskConical,
  Database
} from 'lucide-react';

interface BottomNavProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const BottomNav: React.FC<BottomNavProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutGrid },
    { id: 'predict', label: 'Predict', icon: Smartphone },
    { id: 'model-lab', label: 'Models', icon: FlaskConical },
    { id: 'dataset', label: 'Data', icon: Database },
  ];

  const handleTabChange = (id: string) => {
    setActiveTab(id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <nav 
      className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#FAF5ED]/95 backdrop-blur-md border-t border-[#E2D7C8] px-2 py-1.5 shadow-[0_-4px_16px_rgba(50,35,20,0.06)]"
      style={{ paddingBottom: 'calc(0.4rem + env(safe-area-inset-bottom, 0px))' }}
      aria-label="Mobile Bottom Navigation"
    >
      <div className="flex items-center justify-around max-w-md mx-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => handleTabChange(item.id)}
              className={`flex flex-col items-center justify-center flex-1 py-1 px-1 rounded-xl transition-all duration-200 active:scale-90 cursor-pointer ${
                isActive
                  ? 'text-amber-900 font-semibold'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
              aria-current={isActive ? 'page' : undefined}
            >
              <div
                className={`relative p-1 rounded-lg transition-colors duration-200 ${
                  isActive ? 'bg-amber-100 text-amber-900 shadow-2xs' : 'text-slate-500'
                }`}
              >
                <Icon className="w-5 h-5 stroke-[2.2]" />
                {isActive && (
                  <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-amber-800 rounded-full animate-pulse" />
                )}
              </div>
              <span className={`text-[10px] mt-0.5 tracking-tight ${isActive ? 'font-bold text-amber-950' : 'font-medium'}`}>
                {item.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
