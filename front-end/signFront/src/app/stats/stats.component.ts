import { Component, OnInit } from '@angular/core';
import { StatsService } from '../services/stats.service';
import { Stats } from '../shared/stats';
@Component({
  selector: 'app-sessions',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.scss']
})
export class StatsComponent implements OnInit {
  stats: Stats[];
  constructor(private statsService: StatsService) { }

  ngOnInit(): void {
    this.statsService.getStats()
      .subscribe(data => {console.log(data); this.stats = data['data'];})
  }



}
