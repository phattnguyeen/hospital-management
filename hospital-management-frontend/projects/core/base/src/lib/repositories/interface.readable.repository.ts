import { InjectionToken } from '@angular/core';
import { Observable } from 'rxjs';

export interface IReadableRepository {
  findById<T>(endPoint: string, id: string): Observable<T>;
  findAll<T>(endPoint: string): Observable<T>;
  findInAll<T>(endPoint: string, body: T, options?: {}): Observable<T>;
}

export const READABLE_REPOSITORY = new InjectionToken<IReadableRepository>('READABLE_REPOSITORY');
