import {Component} from '@angular/core';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {

  title="EleNa - Elevation based Navigation";
  originLat = 42.373126;
  originLng = -72.519827;

  destinationLat = 42.373070; 
  destinationLng = -72.501176
  
  origin = { lat: 42.350489, lng: -72.527421 };
  destination = { lat: 42.451643, lng: -72.565172 };
  
  placeMarker($event): void{
    console.log($event);
  }

  endDragOrigin($event: any): void {
    console.log($event);
    this.originLat= $event.coords.lat;
    this.originLng = $event.coords.lng;
  }

  endDragDestination($event: any): void {
    console.log($event);
    this.destinationLat = $event.coords.lat;
    this.destinationLng = $event.coords.lng;
  }
}