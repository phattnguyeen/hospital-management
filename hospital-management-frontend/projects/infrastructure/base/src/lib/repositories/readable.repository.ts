import { HttpClient } from '@angular/common/http';
import { DestroyRef, inject } from '@angular/core';
import { IReadableRepository } from '@core/base';
import { Observable } from 'rxjs';
import { HMSContext } from './hms.context';

export class ReadableRepository implements IReadableRepository {
  protected _context = inject(HMSContext);
  protected httpClient = inject(HttpClient);
  protected destroyRef = inject(DestroyRef);

  protected readonly defaultOptions = {
    headers: {
      'Time-Zone': Intl.DateTimeFormat().resolvedOptions().timeZone,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  };

  private mergeOptions(customOptions?: {}): {} {
    return { ...this.defaultOptions, ...customOptions };
  }

  findAll<T>(endPoint: string, options?: {}): Observable<T> {
    return this.httpClient.get<T>(endPoint, this.mergeOptions(options));
  }

  findById<T>(endPoint: string, id: string, options?: {} | undefined): Observable<T> {
    return this.httpClient.get<T>(endPoint, this.mergeOptions(options));
  }

  findInAll<T>(endPoint: string, body: T, options?: {}): Observable<T> {
    return this.httpClient.post<T>(endPoint, body, this.mergeOptions(options));
  }
}
