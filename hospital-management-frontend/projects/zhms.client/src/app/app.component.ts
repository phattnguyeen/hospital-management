import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Router, RouterOutlet } from '@angular/router';
import { BROWSER_STORAGE } from '@infrastructure/base';
import { TranslateService } from '@ngx-translate/core';
import { SwitchLanguagesService, ViewConstant as ViewConstantLanguage } from '@view/utils';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  private readonly router = inject(Router);
  private readonly _storage = inject(BROWSER_STORAGE);
  private readonly _translateService = inject(TranslateService);
  private readonly _switchLanguagesService = inject(SwitchLanguagesService);

  title = 'zhms.client';
  public isLoading = false;

  constructor() {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationStart) {
        this.isLoading = true;
      } else if (event instanceof NavigationEnd || event instanceof NavigationCancel || event instanceof NavigationError) {
        this.isLoading = false;
      }
    });
  }

  ngOnInit() {
    this.initializeLanguage();
  }

  private initializeLanguage() {
    const language = this._switchLanguagesService.getCurrentLang();
    this._switchLanguagesService.setLanguage(language);
  }
}
