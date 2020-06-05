import {Routes} from '@angular/router'

import { TrainerComponent } from '../trainer/trainer.component';
import { SessionsComponent } from '../sessions/sessions.component';
import { StatsComponent } from '../stats/stats.component';

export const routes: Routes = [
    {path: 'home', component: TrainerComponent},
    {path: 'sessions', component: SessionsComponent},
    {path: 'stats', component: StatsComponent},
    {path: '', redirectTo: 'home', pathMatch: 'full'},
];
