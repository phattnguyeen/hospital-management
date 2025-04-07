import { inject, Injectable, signal } from '@angular/core';
import { AssetQueryHandler, SignInQueryHandler } from '@application/queries';
import { AssetRequest } from '@core/models';
import { ViewContext, ViewDataType } from '@view/base';
import { ViewConstant } from './view.constant';

@Injectable({ providedIn: 'root' })
export class SignInContext extends ViewContext {
  private readonly _signInQueryHandler = inject(SignInQueryHandler);
  private readonly _assetQueryHandler = inject(AssetQueryHandler);

  private logo = signal<any>('');
  private loadLogo() {
    this.executeRequest(this._assetQueryHandler.handle(new AssetRequest())).subscribe((data) => {
      this.logo.set(data);
    });
  }

  setItem(item: ViewDataType): void {}
  getItem(filter?: ViewDataType) {
    if (!filter && !filter.id) return;
    switch (filter.id) {
      case ViewConstant.LOGO:
        return this.logo();
    }
  }
  getViewData(filter?: ViewDataType) {
    if (!filter && !filter.id) return;
    switch (filter.id) {
      case ViewConstant.LOGO:
        return this.loadLogo();
    }
  }
}
