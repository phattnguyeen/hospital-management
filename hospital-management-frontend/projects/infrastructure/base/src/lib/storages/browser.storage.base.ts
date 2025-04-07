export interface BrowserStorageBase {
  get(key: string): any;
  set(key: string, value: string): void;
  remove(key: string): void;
  clear(): void;
}
