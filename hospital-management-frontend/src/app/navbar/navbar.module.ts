import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderNavComponent } from './header-nav/header-nav.component';
import { RouterModule } from '@angular/router';



@NgModule({
  declarations: [
    HeaderNavComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    HeaderNavComponent

  ]
})
export class NavbarModule { }
