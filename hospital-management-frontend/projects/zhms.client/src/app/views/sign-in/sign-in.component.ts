import { CommonModule } from '@angular/common';
import { Component, ElementRef, inject, OnDestroy, OnInit, signal, viewChild } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
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
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'hms-sign-in',
  standalone: true,
  imports: [CommonModule, FormsModule, MatSelectModule, MatInputModule, MatSlideToggleModule, MatButtonModule, ReactiveFormsModule, TranslateModule],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.scss',
  providers: [{ provide: VIEW_CONTEXT, useExisting: SignInContext }],
})
export class SignInComponent extends ViewComponnet implements OnInit, OnDestroy {
  private readonly _switchLanguagesService = inject(SwitchLanguagesService);
  private readonly logoContainer = viewChild<ElementRef>('logoContainer');

  readonly errorMessage = signal<string>('');

  readonly isEnglish = false;

  public readonly signInForm = new FormGroup({
    selected: new FormControl('vi'),
    phone: new FormControl('', [Validators.required, Validators.maxLength(10)]),
    password: new FormControl('', [Validators.required, Validators.minLength(8), Validators.maxLength(255)]),
  });

  ngOnInit(): void {
    this._context.getViewData({ id: ViewConstant.LOGO });
  }

  public login() {
    this._context.save({ id: ViewConstant.LOGIN, username: this.signInForm.controls.phone.value, password: this.signInForm.controls.password.value }, (error) => {
      if (error) {
        this.errorMessage.set(error);
      }
    });
  }

  private eds = explicitEffect([this._context.getItem({ id: ViewConstant.LOGO }), this._context.getItem({ id: ViewConstant.SUCCESS })], ([logo, success]) => {
    if (success) {
      this._router.navigate(['/home'], { replaceUrl: true });
      return;
    }
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

  ngOnDestroy(): void {
    this.eds.destroy();
  }
}
