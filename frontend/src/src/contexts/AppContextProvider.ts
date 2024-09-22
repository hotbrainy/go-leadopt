import { createContext } from "react";

interface AppContextType {
  value: string;
  setValue: (value: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);
export default AppContext;
