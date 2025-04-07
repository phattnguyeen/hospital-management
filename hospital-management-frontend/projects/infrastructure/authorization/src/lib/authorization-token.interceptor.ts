import {  HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BROWSER_STORAGE } from '@infrastructure/base';
import {  Observable } from 'rxjs';
import { AuthorizationConstant } from './authorization.constant';

@Injectable({
  providedIn: 'root',
})
export class AuthorizationTokenInterceptor implements HttpInterceptor {
  private readonly _storage = inject(BROWSER_STORAGE);

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
   const token = this._storage.get(AuthorizationConstant.accessToken);
  if (token) {
    const cloned = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next.handle(cloned);
  }
  return next.handle(req);
  }
}
