import { Injectable } from '@angular/core';
import { BrowserStorageBase } from './browser.storage.base';

@Injectable({ providedIn: 'root' })
export class LocalStorage implements BrowserStorageBase {
  public get(key: string) {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  }
  public set(key: string, value: string): void {
    localStorage.setItem(key, JSON.stringify(value));
  }
  public remove(key: string): void {
    localStorage.removeItem(key);
  }
  public clear(): void {
    localStorage.clear();
  }
}
