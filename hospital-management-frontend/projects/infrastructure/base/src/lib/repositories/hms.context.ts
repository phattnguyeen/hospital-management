import { Injectable, InjectionToken } from '@angular/core';
import { Context } from './context';
import { BrowserStorageBase, LocalStorage } from '../storages';


@Injectable({ providedIn: 'root' })
export class HMSContext implements Context {
  private _endPoint: string = '';

  /**
   * Defines get Endpoint
   */
  public get endPoint() {
    return this._endPoint;
  }

  /**
   * Defines set Endpoint
   */
  public set endPoint(endPoint: string) {
    this._endPoint = endPoint;
  }
}

export const BROWSER_STORAGE = new InjectionToken<BrowserStorageBase>('BROWSER_STORAGE', {
  providedIn: 'root',
  factory: () => new LocalStorage(),
});
