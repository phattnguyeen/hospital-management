import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BreadcrumbService } from 'xng-breadcrumb';
import { NgxSpinnerModule } from 'ngx-spinner';
import { CoreModule } from './core/core.module';
import { AccountModule } from './account/account.module';
import { NavbarModule } from './navbar/navbar.module';
import { DoctorNavComponent } from './navbar/doctor-nav/doctor-nav.component';
import { AppointmentNavComponent } from './navbar/appointment-nav/appointment-nav.component';
import { BlogNavComponent } from './navbar/blog-nav/blog-nav.component';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CoreModule,
    AccountModule,
    NavbarModule,
    DoctorNavComponent,
    AppointmentNavComponent,
    BlogNavComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
