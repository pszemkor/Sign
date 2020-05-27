import { Component, OnInit } from '@angular/core';
import {LetterService} from '../services/letter.service'
@Component({
  selector: 'app-trainer',
  templateUrl: './trainer.component.html',
  styleUrls: ['./trainer.component.scss']
})
export class TrainerComponent implements OnInit {
  private currentLetter: string;
  
  constructor(private letterService: LetterService) { 
  }

  ngOnInit(): void {
    this.letterService.getLetterToRecognize()
    .subscribe(current => this.currentLetter = current)
  }

}
