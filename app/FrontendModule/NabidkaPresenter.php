<?php

namespace App\FrontendModule;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class NabidkaPresenter extends BasePresenter
{
	public function actionDetail($id)
	{
		$this->template->offerDetail = $this->offerEntity->findActive($id);
		
		if (!$this->template->offerDetail) {
			$this->redirect("default");
		}
	}
}
