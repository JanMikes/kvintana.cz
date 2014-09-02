<?php

namespace App\FrontendModule;

use App\Factories\ManageDiscussionFormFactory;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class DiskusePresenter extends BasePresenter
{
	public function renderDefault()
	{
		$this->template->rows = $this->discussionEntity->findActive()->order("id DESC");
	}


	protected function createComponentDiscussionForm(ManageDiscussionFormFactory $factory)
	{
		return $factory->create(null);
	}
}
