<?php

namespace App\FrontendModule;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class SpolupracePresenter extends BasePresenter
{
	public function renderDefault()
	{
		$this->template->partners = $this->partnerEntity->findActive()->order("order DESC");
	}
}
