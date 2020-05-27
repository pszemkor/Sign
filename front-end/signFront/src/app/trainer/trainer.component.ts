import { Component, OnInit } from '@angular/core';
import {LetterService} from '../services/letter.service'
import { Letter } from '../shared/letter';
@Component({
  selector: 'app-trainer',
  templateUrl: './trainer.component.html',
  styleUrls: ['./trainer.component.scss']
})
export class TrainerComponent implements OnInit {
  currentLetter: string = "X";
  
  constructor(private letterService: LetterService) { 
  }

  ngOnInit(): void {
    this.letterService.getLetterToRecognize()
    .subscribe(current => this.currentLetter = current["letter"])
  }

  onStart(){
    this.letterService.getLetterToRecognize()
    .subscribe(current => {console.log(current["letter"]);this.currentLetter = current["letter"]});
  }


}
