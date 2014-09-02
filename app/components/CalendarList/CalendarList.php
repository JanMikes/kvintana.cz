<?php

namespace App\Components;

use App,
	App\Database\Entities\CalendarEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class CalendarList extends Component
{
	use TRecordHandlers;


	public function __construct(CalendarEntity $calendarEntity)
	{
		$this->entity = $calendarEntity;
	}


	public function render($code = null)
	{
		$template = $this->createTemplate();

		$template->rows = $this->entity->findAll();
		$template->inactiveCnt = $this->entity->getInactiveCnt($template->rows);

		$template->render();
	}
}
