export interface MenuInfo {
  key: string;
  keyPath: string[];
  /** @deprecated This will not support in future. You should avoid to use this */
  item: React.ReactInstance;
  domEvent: React.MouseEvent<HTMLElement> | React.KeyboardEvent<HTMLElement>;
}

export interface DataType {
  id: string;
  first_name: string;
  last_name: string;
  company: string;
  position: string;
  linkedin_url: string;
}
 