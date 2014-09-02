<?php

namespace App\Components;

use App,
	App\Database\Entities\GalleryEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class GalleriesList extends Component
{
	use TRecordHandlers;

	private $offerId;
	

	public function __construct($offerId, GalleryEntity $galleryEntity)
	{
		$this->entity = $galleryEntity;
		$this->offerId = $offerId;

		$this->additionalReorderConditions = array(
			"offer_id" => $offerId,
		);
	}


	public function render($code = null)
	{
		$template = $this->createTemplate();

		$template->rows = $this->entity->findAll()->where("offer_id", $this->offerId);
		$template->inactiveCnt = $this->entity->getInactiveCnt($template->rows);

		$template->render();
	}
}
