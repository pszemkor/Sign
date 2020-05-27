import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { TrainerComponent } from './trainer/trainer.component';
import { MatButtonModule } from '@angular/material/button';
import {baseURL} from './shared/base'
import { HttpClientModule } from '@angular/common/http';
@NgModule({
  declarations: [
    AppComponent,
    TrainerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatToolbarModule,
    NoopAnimationsModule,
    MatButtonModule,
    HttpClientModule
  ],
  providers: [{ provide: 'BaseURL', useValue: baseURL }],
  bootstrap: [AppComponent]
})
export class AppModule { }
