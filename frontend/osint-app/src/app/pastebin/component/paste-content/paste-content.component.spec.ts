import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PasteContentComponent } from './paste-content.component';

describe('PasteContentComponent', () => {
  let component: PasteContentComponent;
  let fixture: ComponentFixture<PasteContentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PasteContentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PasteContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
