import { isDevMode, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { provideScrollbarOptions } from 'ngx-scrollbar';
import { environment } from '../environments/environment';
import { HTTP_INTERCEPTORS, HttpClient, provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { AuthorizationTokenInterceptor } from '@infrastructure/authorization';
import { HMSContext } from '@infrastructure/base';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { ServiceWorkerModule } from '@angular/service-worker';

/**
 * To load the json file, it use HttpClient as default.
 * where the location is './i18n/'
 */
export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http, './i18n/', '.json');
}

@NgModule({
  declarations: [AppComponent],
  imports: [
    MatProgressSpinnerModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: HttpLoaderFactory,
        deps: [HttpClient],
      },
    }),
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: !isDevMode(),
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000',
    }),
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthorizationTokenInterceptor,
      multi: true,
    },
    {
      provide: HMSContext,
      useFactory: () => {
        const uri = environment.URI;
        var hmsContext = new HMSContext();
        hmsContext.endPoint = uri;
        return hmsContext;
      },
    },
    provideHttpClient(withInterceptorsFromDi()),
    provideScrollbarOptions({
      visibility: 'hover',
      appearance: 'compact',
      orientation: 'vertical',
    }),
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
