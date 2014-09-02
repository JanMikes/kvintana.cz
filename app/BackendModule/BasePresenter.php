<?php

namespace App\BackendModule;

use App;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
abstract class BasePresenter extends App\BasePresenter
{
	/** @var App\Database\Entities\OfferEntity @autowire */
	protected $offerEntity;


	public function beforeRender()
	{
		parent::beforeRender();
		
		$this->template->menuOffers = $this->offerEntity->findAll();
	}

	/** @return CssLoader */
	protected function createComponentCss()
	{
		return $this->webLoader->createCssLoader('backend');
	}


	/** @return JavaScriptLoader */
	protected function createComponentJs()
	{
		return $this->webLoader->createJavaScriptLoader('backend');
	}
}
