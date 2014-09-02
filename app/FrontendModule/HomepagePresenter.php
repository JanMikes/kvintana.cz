<?php

namespace App\FrontendModule;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class HomepagePresenter extends BasePresenter
{
	public function renderDefault()
	{
		$this->template->aboutRow = $this->aboutEntity->getLast();
	}
}
