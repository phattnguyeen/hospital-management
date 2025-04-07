import { Component, OnInit } from '@angular/core';
import { HeaderNavComponent } from './navbar/header-nav/header-nav.component';
import { MainNavComponent } from './navbar/main-nav/main-nav.component';
import { DoctorNavComponent } from './navbar/doctor-nav/doctor-nav.component';
import { FooterNavComponent } from './navbar/footer-nav/footer-nav.component';
import { AppointmentNavComponent } from './navbar/appointment-nav/appointment-nav.component';

@Component({
  selector: 'hms-home',
  standalone: true,
  imports: [HeaderNavComponent, MainNavComponent, DoctorNavComponent, FooterNavComponent, AppointmentNavComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}
}
