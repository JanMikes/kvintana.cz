<?php

namespace App\FrontendModule;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class FotogaleriePresenter extends BasePresenter
{
	public function renderDefault()
	{
		$this->template->galleries = $this->galleryEntity->findActive()->order("order DESC");
	}


	public function actionDetail($id)
	{
		$this->template->gallery = $this->galleryEntity->findActive($id);
		
		if (!$this->template->gallery) {
			$this->redirect("default");
		}
	}
}
