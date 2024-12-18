import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DoctorNavComponent } from './doctor-nav.component';

describe('DoctorNavComponent', () => {
  let component: DoctorNavComponent;
  let fixture: ComponentFixture<DoctorNavComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DoctorNavComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DoctorNavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
