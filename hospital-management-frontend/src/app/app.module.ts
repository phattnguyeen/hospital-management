import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BreadcrumbService } from 'xng-breadcrumb';
import { NgxSpinnerModule } from 'ngx-spinner';
import { CoreModule } from './core/core.module';
import { NavbarModule } from './navbar/navbar.module';
import { AccountModule } from './account/account.module';
import { LoginComponent } from './account/login/login.component';


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule, // Add HttpClientModule to imports
    CoreModule,
    NavbarModule,
    AccountModule
    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }