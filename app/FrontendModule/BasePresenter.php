<?php

 namespace App\FrontendModule;

use App,
	Nette;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
abstract class BasePresenter extends App\BasePresenter
{
	/** @var App\Database\Entities\OfferEntity @autowire */
	protected $offerEntity;

	/** @var App\Database\Entities\DiscussionEntity @autowire */
	protected $discussionEntity;

	/** @var App\Database\Entities\CalendarEntity @autowire */
	protected $calendarEntity;

	/** @var App\Database\Entities\GalleryEntity @autowire */
	protected $galleryEntity;

	/** @var App\Database\Entities\AboutEntity @autowire */
	protected $aboutEntity;

	/** @var App\Database\Entities\PartnerEntity @autowire */
	protected $partnerEntity;


	protected function beforeRender()
	{
		parent::beforeRender();

		$this->template->offers = $this->offerEntity->findActive();
		$this->template->calendar = $this->calendarEntity->findActive()->order("order DESC");
	}


	/** @return CssLoader */
	protected function createComponentCss()
	{
		return $this->webLoader->createCssLoader('frontend');
	}


	/** @return JavaScriptLoader */
	protected function createComponentJs()
	{
		return $this->webLoader->createJavaScriptLoader('frontend');
	}
}
