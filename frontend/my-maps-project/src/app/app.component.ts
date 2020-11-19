import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-root',
    template:'<agm-marker [latitude]="route[0][0]" [longitude]="route[1][1]" *ngFor="let route of {{routes}}; let i=index"></agm-marker>',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {

  constructor(private http: HttpClient) { }

  title="EleNa - Elevation based Navigation";
  originLat = 42.3504489;
  originLng = -72.5274984;
  data; 
  serverUrl = 'http://localhost:8000/find_route/'
  destinationLat = 42.3777404; 
  destinationLng = -72.5198350;
  locations = [{ lat: 42.350489, lng: -72.527421 }, { lat: 42.451643, lng: -72.565172 }]

  routes;
  elevation_choice;
  percentage_of_shortest_distance = 0;
  
  origin = { lat: 42.350489, lng: -72.527421 };
  destination = { lat: 42.451643, lng: -72.565172 };

  setOriginCoordinates($event: any) {
    console.log($event);
    this.originLat = $event.latLng.lat();;
    this.originLng = $event.latLng.lng();;
  }

  setDestinationCoordinates($event: any) {
    console.log($event);
    this.destinationLat = $event.latLng.lat();;
    this.destinationLng = $event.latLng.lng();;
  }

  onGetDirectionClick(){
    
    console.log("button click recorded")
    console.log("elevation choice selected is", this.elevation_choice)
    console.log("percentage of shortest distance is", this.percentage_of_shortest_distance)
    // this.http.post(this.serverUrl,this.data).toPromise().then(data=>{console.log(data)});
    const headers = { 'content-type': 'application/json'}  
    this.data = {"source_latitude": this.originLat, "source_longitude": this.originLng, "destination_latitude": this.destinationLat, 
    "destination_longitude": this.destinationLng, "percentage": this.percentage_of_shortest_distance, "elevation_type": this.elevation_choice, 
    "algorithm": "yens"}
    const body=JSON.stringify(this.data);
    console.log(body)
    this.http.post(this.serverUrl, body,{'headers':headers}).toPromise()
    .then(
      res => { // Success
        console.log(res);
        this.setRoute(res);
      }
    );
  }

  setRoute(response){
    this.routes = response['route']
    console.log(this.routes)

    this.locations = []
    for (let entry of this.routes) {
      let new_coordinate = {}
      // new_coordinate["lat"] = entry[0];
      // new_coordinate["lng"] = entry[1];
      this.locations.push({"lat": entry[0], "lng": entry[1]});
    }

    console.log(this.locations);
  }

//   public markerOptions = {
//     origin: {
//             draggable: true,
//          },
//     destination: {
//              draggable: true,
//          },
//   }

//   public renderOptions = {
//     suppressMarkers: true,
//  }
 
//  setOriginCoordinates(event)
//     {
//         let coords=JSON.stringify(event);
//         let coords3=JSON.parse(coords);
//         console.log("updated latitude :: "+coords3.lat);
//         console.log("updated longitude :: "+coords3.lng);
//         this.originLat = coords3.lat
//         this.originLng = coords3.lng
//     }

//     setDestinationCoordinates(event)
//     {
//         let coords=JSON.stringify(event);
//         let coords3=JSON.parse(coords);
//         console.log("updated latitude :: "+coords3.lat);
//         console.log("updated longitude :: "+coords3.lng);
//         this.destinationLat = coords3.lat
//         this.destinationLng = coords3.lng
    // } 
  
  // placeMarker($event): void{
  //   console.log($event);
  // }

  // endDragOrigin($event: any): void {
  //   console.log($event);
  //   this.originLat= $event.coords.lat;
  //   this.originLng = $event.coords.lng;

  //   this.locations[0] = {lat:this.originLat, lng:this.originLng}
  // }

  // endDragDestination($event: any): void {
  //   console.log($event);
  //   this.destinationLat = $event.coords.lat;
  //   this.destinationLng = $event.coords.lng;
  // }
}