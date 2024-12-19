import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { initThreeScene } from 'src/app/three/three-scene';
import { LogoService } from 'src/app/service/logo.service';
import lottie from 'lottie-web';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, AfterViewInit {
  @ViewChild('threeContainer', { static: true }) threeContainer!: ElementRef;
  @ViewChild('logoContainer', { static: true }) logoContainer!: ElementRef;

  constructor(private logoService: LogoService) { }

  ngOnInit(): void {
    this.logoService.getLogo().subscribe(data => {
      lottie.loadAnimation({
        container: this.logoContainer.nativeElement,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: data // Adjust this based on the structure of your JSON
      });
    });
  }

  ngAfterViewInit() {
    if (this.threeContainer) {
      initThreeScene(this.threeContainer.nativeElement);
    }
  }
}