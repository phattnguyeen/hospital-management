import { ActionHandlerType, ViewData } from './view.type';

export type ViewOptions = {
  icon?: string;
  title?: string;
  content?: string;
  disableClose?: boolean;

  /** Call back function */
  actionHandler?: (actionHandlerType: ActionHandlerType, data?: ViewData) => void;
};

export type ColorStyle = 'primary' | 'secondary' | 'transparent' | 'success' | 'danger' | 'warning' | 'info' | 'link' | 'bordered' | 'light' | 'dark';
