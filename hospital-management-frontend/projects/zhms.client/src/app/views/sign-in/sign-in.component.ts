import { CommonModule } from '@angular/common';
import { Component, ElementRef, inject, viewChild } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { TranslateModule } from '@ngx-translate/core';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { SwitchLanguagesService, ViewConstant as ViewConstantLanguages } from '@view/utils';
import { VIEW_CONTEXT, ViewComponnet } from '@view/base';
import { SignInContext } from './sign-in.context';
import { ViewConstant } from './view.constant';
import { explicitEffect } from 'ngxtension/explicit-effect';
import lottie from 'lottie-web';

@Component({
  selector: 'hms-sign-in',
  standalone: true,
  imports: [CommonModule, FormsModule, MatInputModule, MatSlideToggleModule, MatButtonModule, ReactiveFormsModule, TranslateModule],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.scss',
  providers: [{ provide: VIEW_CONTEXT, useExisting: SignInContext }],
})
export class SignInComponent extends ViewComponnet {
  private readonly logoContainer = viewChild<ElementRef>('logoContainer');

  username: string = '';
  password: string = '';
  errorMessage: string | null = null;

  isEnglish = false;

  private readonly _switchLanguagesService = inject(SwitchLanguagesService);

  ngAfterViewInit() {}

  public get logo() {
    return this._context.getItem({ id: ViewConstant.LOGO });
  }

  public login() {
    this._context.getViewData({ id: ViewConstant.LOGO });
  }

  eds = explicitEffect([this.logo], ([logo]) => {
    if (logo) {
      lottie.loadAnimation({
        container: this.logoContainer()?.nativeElement,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: logo,
      });
    }
  });

  public toggleLanguage(isEnglish: boolean) {
    const lang = isEnglish ? ViewConstantLanguages.ENGLISH : ViewConstantLanguages.VIETNAMESE;
    this._switchLanguagesService.setLanguage(lang);
  }
}
