import { createContext } from "react";

interface LayoutContextType {
  collapsed: boolean;
  setCollapsed: (value: boolean) => void;
}

const LayoutContext = createContext<LayoutContextType | undefined>(undefined);
export default LayoutContext;
