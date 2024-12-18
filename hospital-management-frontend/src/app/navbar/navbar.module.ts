import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderNavComponent } from './header-nav/header-nav.component';
import { RouterModule } from '@angular/router';
import { FooterNavComponent } from './footer-nav/footer-nav.component';
import { MainNavComponent } from './main-nav/main-nav.component';



@NgModule({
  declarations: [
    HeaderNavComponent,
    FooterNavComponent,
    MainNavComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    HeaderNavComponent,
    FooterNavComponent,
    MainNavComponent

  ]
})
export class NavbarModule { }
