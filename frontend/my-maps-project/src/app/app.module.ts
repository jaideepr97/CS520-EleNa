import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AgmCoreModule } from '@agm/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DirectionsMapDirective } from './directions-map.directive';

@NgModule({
  declarations: [
    AppComponent,

    DirectionsMapDirective
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyANBJfk8OsDGMa7QBR6IIzc2uJn3EqYslo'
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }