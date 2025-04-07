import { inject, Injectable, signal } from '@angular/core';
import { AssetQueryHandler, SignInQueryHandler } from '@application/queries';
import { AssetRequest, SignInErrorResponse, SignInRequest, SignInResponse } from '@core/models';
import { ViewDataType, ViewEditContext } from '@view/base';
import { ViewConstant } from './view.constant';
import { catchError } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { NavigationEnd, RouteConfigLoadEnd } from '@angular/router';
import { AuthorizationConstant } from '@infrastructure/authorization';

@Injectable({ providedIn: 'root' })
export class SignInContext extends ViewEditContext {
  private readonly _signInQueryHandler = inject(SignInQueryHandler);
  private readonly _assetQueryHandler = inject(AssetQueryHandler);

  private readonly logo = signal<any>('');
  private readonly loginSuccess = signal<boolean>(false);

  setItem(item: ViewDataType): void {}
  getItem(filter?: ViewDataType) {
    if (!filter && !filter.id) return;
    switch (filter.id) {
      case ViewConstant.LOGO:
        return this.logo;
      case ViewConstant.SUCCESS:
        return this.loginSuccess;
    }
    return '';
  }
  getViewData(filter?: ViewDataType) {
    if (!filter && !filter.id) return;
    switch (filter.id) {
      case ViewConstant.LOGO:
        return this.loadLogo();
    }
  }

  save(filter?: ViewDataType, onError?: (message: string) => void): void {
    if (!filter && !filter.id) return;
    switch (filter.id) {
      case ViewConstant.LOGIN:
        const request = new SignInRequest();
        request.username = filter.username;
        request.password = filter.password;

        this._signInQueryHandler.handle(request).subscribe((data) => {
          if (data instanceof SignInResponse) {
            this.loginSuccess.set(true);
            this.storage.set(AuthorizationConstant.accessToken, data.access_token);
            this.storage.set(AuthorizationConstant.tokenType, data.token_type);
          }
          if (data instanceof SignInErrorResponse) {
            if (onError) onError(data.detail);
          }
        });
        break;
    }
  }
  remove(filter?: ViewDataType, onError?: (message: string) => void): void {}
  cancel(filter?: ViewDataType, onError?: (message: string) => void): void {}

  private loadLogo() {
    const request = new AssetRequest();
    request.name = 'health-care.json';
    this.executeRequest(this._assetQueryHandler.handle(request))
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((data) => {
        this.logo.set(data);
      });
  }
}
