<?php

namespace App\Components;

use App,
	App\Database\Entities\PartnerEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class PartnersList extends Component
{
	use TRecordHandlers;


	public function __construct(PartnerEntity $partnerEntity)
	{
		$this->entity = $partnerEntity;
	}


	public function render($code = null)
	{
		$template = $this->createTemplate();

		$template->rows = $this->entity->findAll();
		$template->inactiveCnt = $this->entity->getInactiveCnt($template->rows);

		$template->render();
	}
}
