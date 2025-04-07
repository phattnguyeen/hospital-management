import { inject, Injectable } from '@angular/core';
import { ViewConstant } from './view.constant';
import { BROWSER_STORAGE } from '@infrastructure/base';
import { TranslateService } from '@ngx-translate/core';

@Injectable({
  providedIn: 'root',
})
export class SwitchLanguagesService {
  private _translateService = inject(TranslateService);
  private readonly _storage = inject(BROWSER_STORAGE);

  getCurrentLang(): string {
    return this._storage.get('xfw-language');
  }

  setLanguage(lang: string) {
    let language: string | undefined = lang;
    if (language == undefined) {
      language = this._storage.get('xfw-language');
      if (language == undefined) {
        language = ViewConstant.VIETNAMESE;
      } else if (language == ViewConstant.VIETNAMESE) {
        language = ViewConstant.ENGLISH;
      } else {
        language = ViewConstant.VIETNAMESE;
      }
    }
    this._translateService.setDefaultLang(language);
    this._storage.set('hms-language', language);
  }
}
